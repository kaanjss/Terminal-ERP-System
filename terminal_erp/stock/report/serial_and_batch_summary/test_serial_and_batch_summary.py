# Copyright (c) 2026, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestSerialAndBatchSummary(Terminal ERPTestSuite):
	def run_report(self, **extra):
		from terminal_erp.stock.report.serial_and_batch_summary.serial_and_batch_summary import execute

		return execute(terminal_framework._dict(extra))[1]

	@staticmethod
	def _cancel_and_delete_stock_entry(name):
		if not terminal_framework.db.exists("Stock Entry", name):
			return
		doc = terminal_framework.get_doc("Stock Entry", name)
		if doc.docstatus == 1:
			doc.cancel()
		terminal_framework.delete_doc("Stock Entry", name, force=1)

	def test_serial_receipt_listed(self):
		from terminal_erp.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry

		item = "_Test Serialized Item With Series"
		se = make_stock_entry(item_code=item, to_warehouse="Stores - _TC", qty=3, basic_rate=100)
		self.addCleanup(self._cancel_and_delete_stock_entry, se.name)

		data = self.run_report(voucher_no=[se.name], voucher_type="Stock Entry")

		self.assertEqual(len(data), 3)
		self.assertEqual(len({row.serial_no for row in data}), 3)
		for row in data:
			self.assertTrue(row.serial_no)
			self.assertEqual(row.qty, 1)
			self.assertEqual(row.incoming_rate, 100)
			self.assertEqual(row.warehouse, "Stores - _TC")
			self.assertEqual(row.voucher_no, se.name)

	def test_batch_receipt_listed(self):
		from terminal_erp.stock.doctype.item.test_item import make_item
		from terminal_erp.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle import (
			get_batch_from_bundle,
		)
		from terminal_erp.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry

		item = make_item(
			properties={
				"is_stock_item": 1,
				"has_batch_no": 1,
				"create_new_batch": 1,
				"batch_number_series": "SBB-.#####",
			}
		).name
		se = make_stock_entry(item_code=item, to_warehouse="_Test Warehouse - _TC", qty=10, basic_rate=50)
		self.addCleanup(self._cancel_and_delete_stock_entry, se.name)
		batch_no = get_batch_from_bundle(se.items[0].serial_and_batch_bundle)

		data = self.run_report(voucher_no=[se.name], voucher_type="Stock Entry")

		row = next((d for d in data if d.batch_no == batch_no), None)
		self.assertIsNotNone(row)
		self.assertEqual(row.qty, 10)
		self.assertEqual(row.incoming_rate, 50)
		self.assertEqual(row.warehouse, "_Test Warehouse - _TC")
		self.assertEqual(row.voucher_no, se.name)
