# Copyright (c) 2019, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestSellingSettings(Terminal ERPTestSuite):
	def test_defaults_populated(self):
		# Setup default values are not populated on migrate, this test checks
		# if setup was completed correctly
		default = terminal_framework.db.get_single_value("Selling Settings", "maintain_same_rate_action")
		self.assertEqual("Stop", default)
