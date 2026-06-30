# Copyright (c) 2026, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.controllers.item_variant import create_variant
from terminal_erp.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
from terminal_erp.stock.report.item_variant_details.item_variant_details import execute
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestItemVariantDetails(Terminal ERPTestSuite):
	def run_report(self, **extra):
		return execute(terminal_framework._dict(extra))[1]

	def test_variants_listed_for_template(self):
		template = "_Test Variant Item"

		variant = create_variant(template, {"Test Size": "Small"})
		variant.insert(ignore_if_duplicate=True)

		make_stock_entry(
			item_code=variant.name,
			to_warehouse="Stores - _TC",
			qty=5,
			rate=100,
		)

		rows = self.run_report(item=template)

		variant_rows = [row for row in rows if row.get("variant_name") == variant.name]
		self.assertEqual(len(variant_rows), 1)

		row = variant_rows[0]
		self.assertEqual(row.get("test_size"), "Small")
		self.assertEqual(row.get("current_stock"), 5)
		self.assertEqual(row.get("open_orders"), 0)
