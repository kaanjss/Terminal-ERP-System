# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from terminal_framework import _, msgprint

from terminal_erp.stock.services.base_stock_gl_composer import BaseStockGLComposer


class StockReconciliationGLComposer(BaseStockGLComposer):
	"""GL composer for Stock Reconciliation.

	SR carries its own expense_account and cost_center which are passed as
	defaults into the base stock GL composition loop.
	"""

	def compose(self, inventory_account_map: dict | None = None) -> list:
		doc = self.doc
		if not doc.cost_center:
			msgprint(_("Please enter Cost Center"), raise_exception=1)
		return super().compose(inventory_account_map, doc.expense_account, doc.cost_center)
