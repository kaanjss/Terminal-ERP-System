from terminal_erp.tests.utils import Terminal ERPTestSuite
from terminal_erp.utilities.activation import get_level


class TestActivation(Terminal ERPTestSuite):
	def test_activation(self):
		site_info = {"activation": {"activation_level": 0, "sales_data": []}}
		levels = get_level(site_info)
		self.assertTrue(levels)
