# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework
from terminal_framework.utils import add_days, today

from terminal_erp.accounts.report.pos_register.pos_register import execute
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestPOSRegister(Terminal ERPTestSuite):
	def test_report_executes(self):
		# Smoke-guards the raw-SQL -> query-builder port: the report's POS Invoice query must
		# compile and run on both MariaDB and postgres (it returns columns + a row list either way).
		company = terminal_framework.db.get_value("Company", {}, "name")
		columns, data = execute(
			terminal_framework._dict({"company": company, "from_date": add_days(today(), -365), "to_date": today()})
		)
		self.assertTrue(columns)
		self.assertIsInstance(data, list)
