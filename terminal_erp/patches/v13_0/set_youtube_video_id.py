import terminal_framework

from terminal_erp.utilities.doctype.video.video import get_id_from_url


def execute():
	terminal_framework.reload_doc("utilities", "doctype", "video")

	for video in terminal_framework.get_all("Video", fields=["name", "url", "youtube_video_id"]):
		if video.url and not video.youtube_video_id:
			terminal_framework.db.set_value("Video", video.name, "youtube_video_id", get_id_from_url(video.url))
