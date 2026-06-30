# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework

from terminal_erp.accounts.report.budget_variance_report.budget_variance_report import execute
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestBudgetVarianceReport(Terminal ERPTestSuite):
	def test_report_executes(self):
		# Smoke-guards the raw-SQL -> query-builder port: the report query must compile and run on
		# both MariaDB and postgres.
		company = terminal_framework.db.get_value("Company", {}, "name")
		fy = terminal_framework.db.get_value("Fiscal Year", {}, "name", order_by="year_start_date desc")
		columns, *_rest = execute(
			terminal_framework._dict(
				{
					"company": company,
					"from_fiscal_year": fy,
					"to_fiscal_year": fy,
					"period": "Yearly",
					"budget_against": "Cost Center",
				}
			)
		)
		self.assertTrue(columns)
