# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework
from terminal_framework.utils import add_days, getdate, nowdate

from terminal_erp.crm.report.first_response_time_for_opportunity.first_response_time_for_opportunity import (
	execute,
)
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestFirstResponseTimeForOpportunity(Terminal ERPTestSuite):
	def test_avg_first_response_time_row(self):
		"""The report groups Opportunity by Date(creation) and averages first_response_time where it
		is > 0, between from_date and to_date. With a single seeded Opportunity created today and a
		known first_response_time, the report must return a row for today whose averaged value equals
		the seeded duration on both engines (Date(creation) and Avg via the query builder)."""
		response_time = 3600  # seconds (Duration)
		lead_email = "_test_frt_opp@example.com"
		lead_name = "_Test FRT Opportunity Lead"

		lead = terminal_framework.db.exists("Lead", {"email_id": lead_email})
		if not lead:
			lead = (
				terminal_framework.get_doc({"doctype": "Lead", "lead_name": lead_name, "email_id": lead_email})
				.insert(ignore_permissions=True)
				.name
			)

		opportunity = terminal_framework.get_doc(
			{
				"doctype": "Opportunity",
				"opportunity_from": "Lead",
				"party_name": lead,
				"company": "_Test Company",
				"currency": "INR",
				"conversion_rate": 1,
			}
		).insert(ignore_permissions=True)

		# first_response_time is a read-only computed field; set it directly.
		terminal_framework.db.set_value(
			"Opportunity",
			opportunity.name,
			"first_response_time",
			response_time,
			update_modified=False,
		)

		columns, data = execute(
			terminal_framework._dict(from_date=add_days(nowdate(), -1), to_date=add_days(nowdate(), 1))
		)

		# rows are positional lists: [creation_date, avg_response_time]
		today = getdate(nowdate())
		row = next((r for r in data if getdate(r[0]) == today), None)
		self.assertIsNotNone(row, "no report row for today's grouped creation date")
		self.assertEqual(getdate(row[0]), today)
		self.assertEqual(row[1], response_time)
