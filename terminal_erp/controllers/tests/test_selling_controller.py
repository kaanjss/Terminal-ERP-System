# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestSellingControllerConversions(Terminal ERPTestSuite):
	@staticmethod
	def _cancel_and_delete(doctype, name):
		if not terminal_framework.db.exists(doctype, name):
			return
		doc = terminal_framework.get_doc(doctype, name)
		if doc.docstatus == 1:
			doc.cancel()
		terminal_framework.delete_doc(doctype, name, force=1)

	def test_partial_delivery_updates_sales_order_status(self):
		# Submitting a Delivery Note against a Sales Order calls
		# SellingController.get_already_delivered_qty / get_so_qty_and_warehouse and StatusUpdater
		# (per_delivered via coalesce(sum(...))) -- all converted to query builder / ORM here.
		from terminal_erp.selling.doctype.sales_order.mapper import make_delivery_note
		from terminal_erp.selling.doctype.sales_order.test_sales_order import make_sales_order
		from terminal_erp.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry

		se = make_stock_entry(item_code="_Test Item", target="_Test Warehouse - _TC", qty=20, basic_rate=100)
		self.addCleanup(self._cancel_and_delete, "Stock Entry", se.name)

		so = make_sales_order(qty=10)

		dn = make_delivery_note(so.name)
		dn.items[0].qty = 4
		dn.insert()
		dn.submit()
		self.addCleanup(self._cancel_and_delete, "Delivery Note", dn.name)

		so.reload()
		self.assertEqual(so.per_delivered, 40.0)
