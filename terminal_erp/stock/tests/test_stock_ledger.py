# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestStockLedgerConversions(Terminal ERPTestSuite):
	"""Exercises the stock_ledger.py raw-SQL -> query-builder conversions on both engines."""

	def test_set_as_cancel_marks_entries_cancelled(self):
		# set_as_cancel runs an UPDATE (raw SQL -> terminal_framework.qb.update) marking the voucher's SLEs
		# is_cancelled=1. Cancelling a receipt exercises it.
		from terminal_erp.stock.doctype.item.test_item import make_item
		from terminal_erp.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry

		item = make_item("_Test SL Cancel Item", {"is_stock_item": 1}).name
		se = make_stock_entry(item_code=item, target="_Test Warehouse - _TC", qty=5, basic_rate=100)
		# register cleanup before the assertions so the entry is removed even if one fails
		self.addCleanup(self._cancel_and_delete, "Stock Entry", se.name)

		self.assertTrue(terminal_framework.db.exists("Stock Ledger Entry", {"voucher_no": se.name, "is_cancelled": 0}))

		se.cancel()

		self.assertFalse(terminal_framework.db.exists("Stock Ledger Entry", {"voucher_no": se.name, "is_cancelled": 0}))
		self.assertTrue(terminal_framework.db.exists("Stock Ledger Entry", {"voucher_no": se.name, "is_cancelled": 1}))

	def test_get_valuation_rate_returns_last_sle_rate(self):
		# get_valuation_rate's last-valuation lookup (raw SQL -> terminal_framework.qb) returns the most recent
		# valuation_rate for the item+warehouse.
		from terminal_erp.stock.doctype.item.test_item import make_item
		from terminal_erp.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
		from terminal_erp.stock.stock_ledger import get_valuation_rate

		item = make_item("_Test SL Valuation Item", {"is_stock_item": 1}).name
		se = make_stock_entry(item_code=item, target="_Test Warehouse - _TC", qty=10, basic_rate=250)
		self.addCleanup(self._cancel_and_delete, "Stock Entry", se.name)

		rate = get_valuation_rate(item, "_Test Warehouse - _TC", "Stock Entry", "_TEST-NO-SUCH-VOUCHER")
		self.assertEqual(rate, 250)

	def test_get_future_sle_with_negative_qty_runs(self):
		# get_future_sle_with_negative_qty (raw SQL -> terminal_framework.qb) must execute on both engines. With no
		# negative future entry it returns an empty result; this guards the converted query's validity.
		from terminal_framework.utils import now_datetime

		from terminal_erp.stock.stock_ledger import get_future_sle_with_negative_qty

		args = {
			"item_code": "_Test Item",
			"warehouse": "_Test Warehouse - _TC",
			"voucher_no": "_TEST-NO-SUCH-VOUCHER",
			"posting_datetime": now_datetime(),
		}
		self.assertIsInstance(get_future_sle_with_negative_qty(args), list | tuple)

	@staticmethod
	def _cancel_and_delete(doctype, name):
		if not terminal_framework.db.exists(doctype, name):
			return
		doc = terminal_framework.get_doc(doctype, name)
		if doc.docstatus == 1:
			doc.cancel()
		terminal_framework.delete_doc(doctype, name, force=1)
