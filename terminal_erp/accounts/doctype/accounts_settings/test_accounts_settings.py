import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestAccountsSettings(Terminal ERPTestSuite):
	def test_stale_days(self):
		cur_settings = terminal_framework.get_doc("Accounts Settings", "Accounts Settings")
		cur_settings.allow_stale = 0
		cur_settings.stale_days = 0

		self.assertRaises(terminal_framework.ValidationError, cur_settings.save)

		cur_settings.stale_days = -1
		self.assertRaises(terminal_framework.ValidationError, cur_settings.save)
