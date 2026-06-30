# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from terminal_framework.utils import add_days, nowdate

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestPurchaseOrderAnalysis(Terminal ERPTestSuite):
	def test_report_executes_and_lists_po(self):
		# get_data groups by (Purchase Order Item, Purchase Order) while selecting other parent
		# columns; this exercises that GROUP BY so the report stays valid on Postgres (which rejects
		# selecting non-grouped columns).
		from terminal_erp.buying.doctype.purchase_order.test_purchase_order import create_purchase_order
		from terminal_erp.buying.report.purchase_order_analysis.purchase_order_analysis import execute

		po = create_purchase_order(company="_Test Company")

		filters = {
			"company": "_Test Company",
			"from_date": add_days(nowdate(), -1),
			"to_date": add_days(nowdate(), 1),
		}
		result = execute(filters)
		columns, data = result[0], result[1]

		self.assertTrue(columns)
		self.assertIn(po.name, {row.get("purchase_order") for row in data})
