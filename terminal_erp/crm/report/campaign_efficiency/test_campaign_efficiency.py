# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework
from terminal_framework.utils import add_days, nowdate

from terminal_erp.crm.report.campaign_efficiency.campaign_efficiency import execute
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestCampaignEfficiency(Terminal ERPTestSuite):
	def test_lead_count_per_campaign(self):
		"""execute() groups Leads by utm_campaign over a creation-date window and counts leads per
		group. Seed two Leads sharing one distinct UTM Campaign, run the report over a window that
		includes their (now-dated) creation, and assert that campaign's row reports lead_count == 2.
		The group is unique to this test, so the count is exact rather than a tautology, and both
		MariaDB and Postgres must return the same row/value."""
		campaign = "_Test Campaign Eff Campaign"
		if not terminal_framework.db.exists("UTM Campaign", campaign):
			terminal_framework.get_doc({"doctype": "UTM Campaign", "__newname": campaign}).insert(ignore_permissions=True)

		for i in range(2):
			terminal_framework.get_doc(
				{
					"doctype": "Lead",
					"lead_name": f"_Test Campaign Eff Lead {i}",
					"utm_campaign": campaign,
				}
			).insert(ignore_permissions=True)

		# from_date <= creation(now) < to_date + 1 -> window covers the freshly inserted leads
		filters = terminal_framework._dict(
			{
				"from_date": add_days(nowdate(), -7),
				"to_date": add_days(nowdate(), 1),
				"based_on": "utm_campaign",
			}
		)
		columns, data = execute(filters)

		row = next((r for r in data if r.get("utm_campaign") == campaign), None)
		self.assertIsNotNone(row, "campaign row missing from report output")
		self.assertEqual(row["lead_count"], 2)
		# no quotations/orders seeded for these leads -> derived counts are zero
		self.assertEqual(row["quot_count"], 0)
		self.assertEqual(row["order_count"], 0)
