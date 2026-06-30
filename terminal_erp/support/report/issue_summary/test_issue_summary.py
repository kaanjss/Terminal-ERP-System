# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework
from terminal_framework.utils import add_days, today

from terminal_erp.support.report.issue_summary.issue_summary import execute
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestIssueSummary(Terminal ERPTestSuite):
	def test_count_grouped_by_issue_priority(self):
		# Unique Issue Priority so this group is isolated from any pre-existing data.
		priority = "__Test Issue Summary Priority"
		if not terminal_framework.db.exists("Issue Priority", priority):
			terminal_framework.get_doc({"doctype": "Issue Priority", "name": priority}).insert()

		opening_date = today()
		for subject in ("__Test Issue Summary A", "__Test Issue Summary B"):
			terminal_framework.get_doc(
				{
					"doctype": "Issue",
					"subject": subject,
					"priority": priority,
					"status": "Open",
					"opening_date": opening_date,
				}
			).insert()

		filters = terminal_framework._dict(
			{
				"based_on": "Issue Priority",
				"from_date": add_days(opening_date, -1),
				"to_date": add_days(opening_date, 1),
			}
		)

		columns, data, _msg, _chart, _summary = execute(filters)

		# get_rows() emits one row per group keyed on "priority" for based_on == "Issue Priority".
		seeded_row = next((row for row in data if row.get("priority") == priority), None)
		self.assertIsNotNone(
			seeded_row,
			f"expected a summary row for priority {priority!r}, got {[r.get('priority') for r in data]}",
		)

		# Two seeded Open issues -> total_issues == 2 and the "open" status bucket == 2.
		self.assertEqual(seeded_row["total_issues"], 2)
		self.assertEqual(seeded_row["open"], 2)
