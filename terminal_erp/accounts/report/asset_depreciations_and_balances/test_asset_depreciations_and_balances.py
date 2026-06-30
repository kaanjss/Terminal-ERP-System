# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework

from terminal_erp.accounts.report.asset_depreciations_and_balances.asset_depreciations_and_balances import (
	execute,
)
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestAssetDepreciationsAndBalancesReport(Terminal ERPTestSuite):
	def test_report_runs_on_both_engines(self):
		"""The report compared IfNull(asset.disposal_date, 0) against 0 -- coalescing a DATE
		column with integer 0. Postgres rejects that (COALESCE types date and integer cannot be
		matched) at plan time, so the whole report errored there regardless of data. It must run
		on both engines."""
		for group_by in ("Asset Category", "Asset"):
			filters = terminal_framework._dict(
				company="_Test Company",
				from_date="2020-01-01",
				to_date="2030-12-31",
				group_by=group_by,
			)
			result = execute(filters)
			self.assertIsInstance(result[1], list)
