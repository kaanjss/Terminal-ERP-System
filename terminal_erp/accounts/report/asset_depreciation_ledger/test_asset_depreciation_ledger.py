# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework

from terminal_erp.accounts.report.asset_depreciation_ledger.asset_depreciation_ledger import execute
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestAssetDepreciationLedger(Terminal ERPTestSuite):
	def test_report_executes(self):
		# Smoke-guards the raw-SQL -> query-builder port: the report query must compile and run on
		# both MariaDB and postgres.
		company = terminal_framework.db.get_value("Company", {}, "name")
		columns, *_rest = execute(
			terminal_framework._dict({"company": company, "from_date": "2020-01-01", "to_date": "2030-12-31"})
		)
		self.assertTrue(columns)
