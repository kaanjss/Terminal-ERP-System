# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework
from terminal_framework.utils import add_days, today

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestStockControllerConversions(Terminal ERPTestSuite):
	@staticmethod
	def _cancel_and_delete(doctype, name):
		if not terminal_framework.db.exists(doctype, name):
			return
		doc = terminal_framework.get_doc(doctype, name)
		if doc.docstatus == 1:
			doc.cancel()
		terminal_framework.delete_doc(doctype, name, force=1)

	def test_future_sle_exists_detects_later_entries(self):
		# future_sle_exists / get_conditions_to_validate_future_sle were converted to query builder
		# (Count + Criterion.any). A later SLE for the same item+warehouse must be detected, which
		# exercises the converted GROUP BY query on both engines.
		from terminal_erp.controllers.stock_controller import future_sle_exists
		from terminal_erp.stock.doctype.item.test_item import make_item
		from terminal_erp.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry

		item = make_item("_Test Future SLE Item", {"is_stock_item": 1}).name
		se = make_stock_entry(item_code=item, target="_Test Warehouse - _TC", qty=10, basic_rate=100)
		self.addCleanup(self._cancel_and_delete, "Stock Entry", se.name)

		# Pretend a different voucher posts a day earlier for the same item/warehouse: the existing
		# (later) SLE must be reported as a future entry.
		args = terminal_framework._dict(
			voucher_type="Stock Entry",
			voucher_no="_TEST-NONEXISTENT-SE",
			posting_date=add_days(today(), -1),
			posting_time="00:00:00",
		)
		sl_entries = [terminal_framework._dict(item_code=item, warehouse="_Test Warehouse - _TC")]

		self.assertTrue(future_sle_exists(args, sl_entries))
