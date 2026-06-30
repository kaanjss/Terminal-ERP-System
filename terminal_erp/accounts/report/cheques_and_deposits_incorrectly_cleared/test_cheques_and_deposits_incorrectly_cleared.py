# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework
from terminal_framework.utils import nowdate

from terminal_erp.accounts.report.cheques_and_deposits_incorrectly_cleared.cheques_and_deposits_incorrectly_cleared import (
	execute,
)
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestChequesAndDepositsIncorrectlyCleared(Terminal ERPTestSuite):
	def test_report_executes_with_case_amount(self):
		# Exercises the Payment Entry branch whose amount column uses a db-aware CASE expression
		# (previously a MySQL-only IF()). IF() does not compile on postgres, so running the report
		# query guards the portability fix on both databases.
		company = terminal_framework.db.get_value("Company", {}, "name")
		account = terminal_framework.db.get_value(
			"Account", {"account_type": "Bank", "company": company, "is_group": 0}, "name"
		)
		columns, data = execute(terminal_framework._dict({"account": account, "report_date": nowdate()}))
		self.assertTrue(columns)
		self.assertIsInstance(data, list)
