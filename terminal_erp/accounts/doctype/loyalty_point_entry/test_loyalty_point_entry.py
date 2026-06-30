# Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework
from terminal_framework.query_builder.functions import Sum
from terminal_framework.utils import today

from terminal_erp.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestLoyaltyPointEntry(Terminal ERPTestSuite):
	def setUp(self):
		# Create test records
		self.loyalty_program_name = "Test Single Loyalty"
		self.customer_name = "Test Loyalty Customer"
		customer = terminal_framework.get_doc("Customer", self.customer_name)
		customer.loyalty_program = self.loyalty_program_name
		customer.save()

	def create_test_invoice(self, redeem=None):
		if redeem:
			si = create_sales_invoice(customer=self.customer_name, qty=1, rate=100, do_not_save=True)
			si.redeem_loyalty_points = True
			si.loyalty_points = redeem
			return si.insert().submit()
		else:
			si = create_sales_invoice(customer=self.customer_name, qty=10, rate=1000, do_not_save=True)
			return si.insert().submit()

	def test_add_loyalty_points(self):
		self.create_test_invoice()
		doc = terminal_framework.get_last_doc("Loyalty Point Entry")
		self.assertEqual(doc.loyalty_points, 10)

	def test_add_loyalty_points_with_discretionary_reason(self):
		doc = terminal_framework.get_doc(
			{
				"doctype": "Loyalty Point Entry",
				"loyalty_program": "Test Single Loyalty",
				"loyalty_program_tier": "Bronce",
				"customer": self.customer_name,
				"invoice_type": "Sales Invoice",
				"loyalty_points": 75,
				"expiry_date": today(),
				"posting_date": today(),
				"company": "_Test Company",
				"discretionary_reason": "Customer Appreciation",
			}
		)
		doc.insert(ignore_permissions=True)
		self.assertEqual(doc.loyalty_points, 75)
		self.assertEqual(doc.discretionary_reason, "Customer Appreciation")

		# Verify the entry in the database
		entry = terminal_framework.get_doc("Loyalty Point Entry", doc.name)
		self.assertEqual(entry.loyalty_points, 75)
		self.assertEqual(entry.discretionary_reason, "Customer Appreciation")

	def test_redeem_loyalty_points(self):
		self.create_test_invoice()
		self.create_test_invoice(redeem=7)
		doc = terminal_framework.get_last_doc("Loyalty Point Entry")
		self.assertEqual(doc.loyalty_points, -7)

		# Check balance
		lpe = terminal_framework.qb.DocType("Loyalty Point Entry")
		balance = (
			terminal_framework.qb.from_(lpe).select(Sum(lpe.loyalty_points)).where(lpe.customer == self.customer_name)
		).run()[0][0]

		self.assertEqual(balance, 3)  # 10 added, 7 redeemed
