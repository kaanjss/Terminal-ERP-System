# Copyright (c) 2021, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework
from terminal_framework.utils import random_string

from terminal_erp.crm.doctype.lead.lead import add_lead_to_prospect
from terminal_erp.crm.doctype.lead.test_lead import make_lead
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestProspect(Terminal ERPTestSuite):
	def test_add_lead_to_prospect_and_address_linking(self):
		company = "_Test Company"
		lead_doc = make_lead()
		address_doc = make_address(address_title=lead_doc.name)
		address_doc.append("links", {"link_doctype": lead_doc.doctype, "link_name": lead_doc.name})
		address_doc.save()
		prospect_doc = make_prospect(company=company, company_name=company)
		add_lead_to_prospect(lead_doc.name, prospect_doc.name)
		prospect_doc.reload()
		lead_exists_in_prosoect = False
		for rec in prospect_doc.get("leads"):
			if rec.lead == lead_doc.name:
				lead_exists_in_prosoect = True
		self.assertEqual(lead_exists_in_prosoect, True)
		address_doc.reload()
		self.assertEqual(address_doc.has_link("Prospect", prospect_doc.name), True)

	def test_make_customer_from_prospect(self):
		from terminal_erp.crm.doctype.prospect.prospect import make_customer as make_customer_from_prospect

		terminal_framework.delete_doc_if_exists("Customer", "_Test Prospect")

		prospect = terminal_framework.get_doc(
			{
				"doctype": "Prospect",
				"company_name": "_Test Prospect",
				"customer_group": "_Test Customer Group",
				"company": "_Test Company",
			}
		)
		prospect.insert()

		customer = make_customer_from_prospect("_Test Prospect")

		self.assertEqual(customer.doctype, "Customer")
		self.assertEqual(customer.company_name, "_Test Prospect")
		self.assertEqual(customer.customer_group, "_Test Customer Group")

		customer.company = "_Test Company"
		customer.insert()

	def test_get_notification_email(self):
		admin_email = terminal_framework.db.get_value("User", "Administrator", "email")
		prospect = terminal_framework.new_doc("Prospect")
		prospect.prospect_owner = "Administrator"
		self.assertEqual(prospect.get_notification_email(), admin_email)

		prospect.prospect_owner = None
		self.assertIsNone(prospect.get_notification_email())


def make_prospect(**args):
	args = terminal_framework._dict(args)

	prospect_doc = terminal_framework.get_doc(
		{
			"doctype": "Prospect",
			"company_name": args.company_name or f"_Test Company {random_string(3)}",
			"company": args.company,
		}
	).insert()

	return prospect_doc


def make_address(**args):
	args = terminal_framework._dict(args)

	address_doc = terminal_framework.get_doc(
		{
			"doctype": "Address",
			"address_title": args.address_title or "Address Title",
			"address_type": args.address_type or "Billing",
			"city": args.city or "Mumbai",
			"address_line1": args.address_line1 or "Vidya Vihar West",
			"country": args.country or "India",
		}
	).insert()

	return address_doc
