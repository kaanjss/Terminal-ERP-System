import terminal_framework

import terminal_erp
from terminal_erp.tests.utils import Terminal ERPTestSuite


@terminal_erp.allow_regional
def test_method():
	return "original"


class TestInit(Terminal ERPTestSuite):
	def test_regional_overrides(self):
		terminal_framework.flags.country = "Maldives"
		self.assertEqual(test_method(), "original")
