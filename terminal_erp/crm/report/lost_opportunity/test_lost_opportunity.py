# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework
from terminal_framework.utils import add_days, today

from terminal_erp.crm.report.lost_opportunity.lost_opportunity import execute
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestLostOpportunity(Terminal ERPTestSuite):
	def test_report_aggregates_lost_reasons(self):
		# Exercises the db-aware GROUP_CONCAT (MariaDB) / STRING_AGG (postgres) aggregation of the
		# child "Opportunity Lost Reason Detail" rows. The MySQL-only GROUP_CONCAT term would fail to
		# compile on postgres, so simply running the report query guards the portability fix on both
		# databases.
		company = terminal_framework.db.get_value("Company", {}, "name")
		columns, data = execute(
			terminal_framework._dict({"company": company, "from_date": add_days(today(), -365), "to_date": today()})
		)
		self.assertTrue(columns)
		self.assertIsInstance(data, list)
