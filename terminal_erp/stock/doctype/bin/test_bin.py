# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.stock.doctype.item.test_item import make_item
from terminal_erp.stock.utils import _create_bin
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestBin(Terminal ERPTestSuite):
	def test_concurrent_inserts(self):
		"""Ensure no duplicates are possible in case of concurrent inserts"""
		item_code = "_TestConcurrentBin"
		make_item(item_code)
		warehouse = "_Test Warehouse - _TC"

		bin1 = terminal_framework.get_doc(doctype="Bin", item_code=item_code, warehouse=warehouse)
		bin1.insert()

		bin2 = terminal_framework.get_doc(doctype="Bin", item_code=item_code, warehouse=warehouse)
		terminal_framework.db.savepoint("dup_bin")
		with self.assertRaises(terminal_framework.UniqueValidationError):
			bin2.insert()
		terminal_framework.db.rollback(save_point="dup_bin")  # preserve transaction in postgres

		# util method should handle it
		bin = _create_bin(item_code, warehouse)
		self.assertEqual(bin.item_code, item_code)

	def test_index_exists(self):
		# has_index is db-agnostic; raw "SHOW INDEX" is MySQL-only and errors on Postgres
		if not terminal_framework.db.has_index("tabBin", "unique_item_warehouse"):
			self.fail("Expected unique index on item-warehouse")
