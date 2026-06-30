# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework
from terminal_framework import _
from terminal_framework.contacts.doctype.address.address import get_default_address
from terminal_framework.contacts.doctype.contact.contact import get_default_contact
from terminal_framework.email.inbox import link_communication_to_document
from terminal_framework.model.document import Document
from terminal_framework.model.mapper import get_mapped_doc


@terminal_framework.whitelist()
def make_customer(source_name: str, target_doc: str | Document | None = None):
	return _make_customer(source_name, target_doc)


def _make_customer(
	source_name: str, target_doc: str | Document | None = None, ignore_permissions: bool = False
):
	def set_missing_values(source, target):
		if source.company_name:
			target.customer_type = "Company"
			target.customer_name = source.company_name
		else:
			target.customer_type = "Individual"
			target.customer_name = source.lead_name

		if not target.customer_group:
			target.customer_group = terminal_framework.db.get_default("Customer Group")

		address = get_default_address("Lead", source.name)
		contact = get_default_contact("Lead", source.name)
		if address:
			target.customer_primary_address = address
		if contact:
			target.customer_primary_contact = contact

	doclist = get_mapped_doc(
		"Lead",
		source_name,
		{
			"Lead": {
				"doctype": "Customer",
				"field_map": {
					"name": "lead_name",
					"company_name": "customer_name",
					"contact_no": "phone_1",
					"fax": "fax_1",
				},
				"field_no_map": ["disabled"],
			}
		},
		target_doc,
		set_missing_values,
		ignore_permissions=ignore_permissions,
	)

	return doclist


@terminal_framework.whitelist()
def make_opportunity(source_name: str, target_doc: str | Document | None = None):
	def set_missing_values(source, target):
		_set_missing_values(source, target)

	target_doc = get_mapped_doc(
		"Lead",
		source_name,
		{
			"Lead": {
				"doctype": "Opportunity",
				"field_map": {
					"doctype": "opportunity_from",
					"name": "party_name",
					"lead_name": "contact_display",
					"company_name": "customer_name",
					"email_id": "contact_email",
					"mobile_no": "contact_mobile",
					"lead_owner": "opportunity_owner",
					"notes": "notes",
				},
			}
		},
		target_doc,
		set_missing_values,
	)

	return target_doc


@terminal_framework.whitelist()
def make_quotation(source_name: str, target_doc: str | Document | None = None):
	def set_missing_values(source, target):
		_set_missing_values(source, target)

	target_doc = get_mapped_doc(
		"Lead",
		source_name,
		{"Lead": {"doctype": "Quotation", "field_map": {"name": "party_name"}}},
		target_doc,
		set_missing_values,
	)

	target_doc.quotation_to = "Lead"
	target_doc.run_method("set_missing_values")
	target_doc.run_method("set_other_charges")
	target_doc.run_method("calculate_taxes_and_totals")

	return target_doc


@terminal_framework.whitelist()
def make_lead_from_communication(communication: str, ignore_communication_links: bool = False):
	"""raise a issue from email"""

	doc = terminal_framework.get_doc("Communication", communication)
	lead_name = None
	if doc.sender:
		lead_name = terminal_framework.db.get_value("Lead", {"email_id": doc.sender})
	if not lead_name and doc.phone_no:
		lead_name = terminal_framework.db.get_value("Lead", {"mobile_no": doc.phone_no})
	if not lead_name:
		lead = terminal_framework.get_doc(
			{
				"doctype": "Lead",
				"lead_name": doc.sender_full_name,
				"email_id": doc.sender,
				"mobile_no": doc.phone_no,
			}
		)
		lead.flags.ignore_mandatory = True
		lead.insert()

		lead_name = lead.name

	link_communication_to_document(doc, "Lead", lead_name, ignore_communication_links)
	return lead_name


def _set_missing_values(source, target):
	address = terminal_framework.get_all(
		"Dynamic Link",
		{
			"link_doctype": source.doctype,
			"link_name": source.name,
			"parenttype": "Address",
		},
		["parent"],
		limit=1,
	)

	contact = terminal_framework.get_all(
		"Dynamic Link",
		{
			"link_doctype": source.doctype,
			"link_name": source.name,
			"parenttype": "Contact",
		},
		["parent"],
		limit=1,
	)

	if address:
		target.customer_address = address[0].parent

	if contact:
		target.contact_person = contact[0].parent
