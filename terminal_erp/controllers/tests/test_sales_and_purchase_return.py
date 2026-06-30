# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestSalesAndPurchaseReturn(Terminal ERPTestSuite):
	@staticmethod
	def _cancel_and_delete(doctype, name):
		if not terminal_framework.db.exists(doctype, name):
			return
		doc = terminal_framework.get_doc(doctype, name)
		if doc.docstatus == 1:
			doc.cancel()
		terminal_framework.delete_doc(doctype, name, force=1)

	def test_sales_return_validates_against_original(self):
		# Submitting a return Delivery Note runs validate_returned_items (Item / Packed Item lookups
		# via terminal_framework.get_all) and get_already_returned_items (qb GROUP BY of the returned qty) -- both
		# converted from raw SQL here. Exercises them on both engines.
		from terminal_erp.stock.doctype.delivery_note.mapper import make_sales_return
		from terminal_erp.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
		from terminal_erp.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry

		se = make_stock_entry(item_code="_Test Item", target="_Test Warehouse - _TC", qty=20, basic_rate=100)
		self.addCleanup(self._cancel_and_delete, "Stock Entry", se.name)

		dn = create_delivery_note(qty=5)
		self.addCleanup(self._cancel_and_delete, "Delivery Note", dn.name)

		return_dn = make_sales_return(dn.name)
		return_dn.insert()
		return_dn.submit()
		self.addCleanup(self._cancel_and_delete, "Delivery Note", return_dn.name)

		self.assertEqual(return_dn.is_return, 1)
		self.assertEqual(return_dn.items[0].qty, -5)
