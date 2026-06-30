# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite
from terminal_erp.utilities.report.youtube_interactions.youtube_interactions import execute


class TestYoutubeInteractions(Terminal ERPTestSuite):
	def test_zero_view_video_is_listed(self):
		"""The original report filtered `WHERE view_count is not null`. The conversion keeps that exact
		semantics with `.where(video.view_count.isnotnull())` (IS NOT NULL), NOT a `<> 0` test, so a
		video with exactly 0 views is still reported. This guards against a regression to `!= 0`
		(which would silently drop 0-view videos) and confirms the filter renders identically on both
		engines."""
		terminal_framework.db.set_single_value("Video Settings", "enable_youtube_tracking", 1)

		for title, views in (("_Test Zero Views Video", 0.0), ("_Test Ten Views Video", 10.0)):
			if terminal_framework.db.exists("Video", title):
				terminal_framework.delete_doc("Video", title, force=True)
			terminal_framework.get_doc(
				{
					"doctype": "Video",
					"title": title,
					"provider": "Vimeo",  # skips the YouTube API call in validate()
					"url": f"https://vimeo.com/{int(views)}",
					"description": title,
					"publish_date": "2024-01-15",
					"view_count": views,
				}
			).insert()

		_columns, data, *_rest = execute(terminal_framework._dict({"from_date": "2024-01-01", "to_date": "2024-12-31"}))
		titles = {row.get("title") for row in data}
		self.assertIn("_Test Ten Views Video", titles)
		# a real, freshly-synced video with 0 views must still be reported
		self.assertIn("_Test Zero Views Video", titles)
