# Copyright (c) 2013, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework
from terminal_framework.utils import add_days, getdate, now_datetime

from terminal_erp.support.report.first_response_time_for_issues.first_response_time_for_issues import (
	execute,
)
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestFirstResponseTimeForIssues(Terminal ERPTestSuite):
	def test_avg_first_response_time_grouped_by_creation_date(self):
		today = getdate()

		# Isolate today's group: any pre-existing Issue created today (from other
		# fixtures running in the same transaction) would pollute the average.
		# Rolled back automatically in tearDown.
		terminal_framework.db.delete("Issue", {"creation": (">=", today)})

		# Seed exactly one Issue created today.
		issue = terminal_framework.get_doc(
			{
				"doctype": "Issue",
				"subject": "First Response Time Report Issue",
				"raised_by": "test_frt_report@example.com",
				"description": "First Response Time Report Issue",
				"company": "_Test Company",
				"creation": now_datetime(),
			}
		).insert(ignore_permissions=True)

		# first_response_time is a read-only computed Duration (seconds); set directly.
		response_time = 3600
		terminal_framework.db.set_value("Issue", issue.name, "first_response_time", response_time)

		columns, data = execute(terminal_framework._dict(from_date=add_days(today, -1), to_date=add_days(today, 1)))

		# Rows are tuples: (creation_date, avg_response_time) -- report uses .run() w/o as_dict.
		rows_for_today = [row for row in data if getdate(row[0]) == today]
		self.assertEqual(
			len(rows_for_today),
			1,
			f"expected exactly one grouped row for {today}, got {rows_for_today}",
		)

		creation_date, avg_response_time = rows_for_today[0]
		self.assertEqual(getdate(creation_date), today)
		self.assertEqual(float(avg_response_time), float(response_time))
