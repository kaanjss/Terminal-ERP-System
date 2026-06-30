import terminal_framework
from terminal_framework import qb

from terminal_erp.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from terminal_erp.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
from terminal_erp.accounts.report.payment_ledger.payment_ledger import execute
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestPaymentLedger(Terminal ERPTestSuite):
	def setUp(self):
		self.company = "_Test Company"
		self.cost_center = "Main - _TC"
		self.warehouse = "Stores - _TC"
		self.income_account = "Sales - _TC"
		self.expense_account = "Cost of Goods Sold - _TC"
		self.debit_to = "Debtors - _TC"

	def test_unpaid_invoice_outstanding(self):
		sinv = create_sales_invoice(
			company=self.company,
			debit_to=self.debit_to,
			expense_account=self.expense_account,
			cost_center=self.cost_center,
			income_account=self.income_account,
			warehouse=self.warehouse,
		)
		get_payment_entry(sinv.doctype, sinv.name).save().submit()

		filters = terminal_framework._dict({"company": self.company})
		columns, data = execute(filters=filters)
		outstanding = [x for x in data if x.get("against_voucher_no") == "Outstanding:"]
		self.assertEqual(outstanding[0].get("amount"), 0)
