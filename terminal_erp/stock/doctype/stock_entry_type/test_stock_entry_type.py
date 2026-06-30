# Copyright (c) 2019, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestStockEntryType(Terminal ERPTestSuite):
	def test_stock_entry_type_non_standard(self):
		stock_entry_type = "Test Manufacturing"

		doc = terminal_framework.get_doc(
			{
				"doctype": "Stock Entry Type",
				"__newname": stock_entry_type,
				"purpose": "Manufacture",
				"is_standard": 1,
			}
		)

		self.assertRaises(terminal_framework.ValidationError, doc.insert)

	def test_stock_entry_type_is_standard(self):
		for stock_entry_type in [
			"Material Issue",
			"Material Receipt",
			"Material Transfer",
			"Material Transfer for Manufacture",
			"Material Consumption for Manufacture",
			"Manufacture",
			"Repack",
			"Send to Subcontractor",
		]:
			self.assertTrue(terminal_framework.db.get_value("Stock Entry Type", stock_entry_type, "is_standard"))
