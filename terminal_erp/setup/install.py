# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import os

import terminal_framework
from terminal_framework.custom.doctype.custom_field.custom_field import create_custom_fields
from terminal_framework.desk.page.setup_wizard.setup_wizard import add_all_roles_to

from terminal_erp.setup.doctype.incoterm.incoterm import create_incoterms
from terminal_erp.setup.utils import identity as _

from .default_success_action import get_default_success_action

default_mail_footer = """<div style="padding: 7px; text-align: right; color: #888"><small>Sent via
	<a style="color: #888" href="http://terminal_framework.io/terminal_erp">Terminal ERP</a></div>"""


def after_install():
	if not terminal_framework.db.exists("Role", "Analytics"):
		terminal_framework.get_doc({"doctype": "Role", "role_name": "Analytics"}).insert()

	set_single_defaults()
	setup_repost_defaults()
	create_print_setting_custom_fields()
	create_marketing_campaign_custom_fields()
	create_address_and_contact_custom_fields()
	create_custom_company_links()
	add_all_roles_to("Administrator")
	create_default_success_action()
	create_incoterms()
	create_default_role_profiles()
	add_company_to_session_defaults()
	add_standard_navbar_items()
	add_app_name()
	update_roles()
	make_default_operations()
	update_pegged_currencies()
	set_default_print_formats()
	toggle_hidden_fields()
	terminal_framework.db.commit()


def make_default_operations():
	for operation in ["Assembly"]:
		if not terminal_framework.db.exists("Operation", operation):
			doc = terminal_framework.get_doc({"doctype": "Operation", "name": operation})
			doc.flags.ignore_mandatory = True
			doc.insert(ignore_permissions=True)


def set_single_defaults():
	for dt in (
		"Accounts Settings",
		"Print Settings",
		"Buying Settings",
		"Selling Settings",
		"Stock Settings",
	):
		default_values = terminal_framework.get_all(
			"DocField", filters={"parent": dt}, fields=["fieldname", "default"], as_list=True
		)
		if default_values:
			try:
				doc = terminal_framework.get_doc(dt, dt)
				for fieldname, value in default_values:
					doc.set(fieldname, value)
				doc.flags.ignore_mandatory = True
				doc.save()
			except terminal_framework.ValidationError:
				pass

	setup_currency_exchange()


def setup_repost_defaults():
	accounts_settings = terminal_framework.get_doc("Accounts Settings")
	for x in terminal_framework.get_hooks("repost_allowed_doctypes"):
		accounts_settings.append("repost_allowed_types", {"document_type": x})
	accounts_settings.save()


def setup_currency_exchange():
	ces = terminal_framework.get_single("Currency Exchange Settings")
	try:
		ces.service_provider = "frankfurter.dev - v2"
		ces.save()
	except terminal_framework.ValidationError:
		pass


def create_print_setting_custom_fields():
	create_custom_fields(
		{
			"Print Settings": [
				{
					"label": _("Compact Item Print"),
					"fieldname": "compact_item_print",
					"fieldtype": "Check",
					"default": "1",
					"insert_after": "with_letterhead",
				},
				{
					"label": _("Print UOM after Quantity"),
					"fieldname": "print_uom_after_quantity",
					"fieldtype": "Check",
					"default": "0",
					"insert_after": "compact_item_print",
				},
				{
					"label": _("Print taxes with zero amount"),
					"fieldname": "print_taxes_with_zero_amount",
					"fieldtype": "Check",
					"default": "0",
					"insert_after": "allow_print_for_cancelled",
				},
			]
		}
	)


def create_marketing_campaign_custom_fields():
	create_custom_fields(
		{
			"UTM Campaign": [
				{
					"label": _("Messaging CRM Campaign"),
					"fieldname": "crm_campaign",
					"fieldtype": "Link",
					"options": "Campaign",
					"insert_after": "campaign_description",
				},
			]
		}
	)


def create_address_and_contact_custom_fields():
	create_custom_fields(
		{
			"Address": [
				{
					"label": _("Tax Category"),
					"fieldname": "tax_category",
					"fieldtype": "Link",
					"options": "Tax Category",
					"insert_after": "fax",
				},
				{
					"label": _("Is Your Company Address"),
					"fieldname": "is_your_company_address",
					"fieldtype": "Check",
					"default": "0",
					"insert_after": "linked_with",
				},
			],
			"Contact": [
				{
					"label": _("Is Billing Contact"),
					"fieldname": "is_billing_contact",
					"fieldtype": "Check",
					"insert_after": "is_primary_contact",
				},
			],
		}
	)


def create_default_success_action():
	for success_action in get_default_success_action():
		if not terminal_framework.db.exists("Success Action", success_action.get("ref_doctype")):
			doc = terminal_framework.get_doc(success_action)
			doc.insert(ignore_permissions=True)


def create_custom_company_links():
	"""Add link fields to Company in Email Account and Communication.

	These DocTypes are provided by the Terminal Framework Framework but need to be associated
	with a company in Terminal ERP to allow for multitenancy. I.e. one company should
	not be able to access emails and communications from another company.
	"""
	create_custom_fields(
		{
			"Email Account": [
				{
					"label": _("Company"),
					"fieldname": "company",
					"fieldtype": "Link",
					"options": "Company",
					"insert_after": "email_id",
				},
			],
			"Communication": [
				{
					"label": _("Company"),
					"fieldname": "company",
					"fieldtype": "Link",
					"options": "Company",
					"insert_after": "email_account",
					"fetch_from": "email_account.company",
					"read_only": 1,
				},
			],
		},
	)


def add_company_to_session_defaults():
	settings = terminal_framework.get_single("Session Default Settings")
	settings.append("session_defaults", {"ref_doctype": "Company"})
	settings.save()


def add_standard_navbar_items():
	navbar_settings = terminal_framework.get_single("Navbar Settings")
	terminal_erp_navbar_items = [
		{
			"item_label": _("Documentation"),
			"item_type": "Route",
			"route": "https://docs.terminal_erp.com/",
			"is_standard": 1,
		},
		{
			"item_label": _("User Forum"),
			"item_type": "Route",
			"route": "https://discuss.terminal_framework.io",
			"is_standard": 1,
		},
		{
			"item_label": _("Terminal Framework School"),
			"item_type": "Route",
			"route": "https://terminal_framework.io/school?utm_source=in_app",
			"is_standard": 1,
		},
		{
			"item_label": _("Report an Issue"),
			"item_type": "Route",
			"route": "https://github.com/terminal_framework/terminal_erp/issues",
			"is_standard": 1,
		},
	]

	current_navbar_items = navbar_settings.help_dropdown
	navbar_settings.set("help_dropdown", [])

	for item in terminal_erp_navbar_items:
		current_labels = [item.get("item_label") for item in current_navbar_items]
		if item.get("item_label") not in current_labels:
			navbar_settings.append("help_dropdown", item)

	for item in current_navbar_items:
		navbar_settings.append(
			"help_dropdown",
			{
				"item_label": item.item_label,
				"item_type": item.item_type,
				"route": item.route,
				"action": item.action,
				"is_standard": item.is_standard,
				"hidden": item.hidden,
			},
		)

	navbar_settings.save()


def add_app_name():
	terminal_framework.db.set_single_value("System Settings", "app_name", "Terminal ERP")


def update_roles():
	website_user_roles = ("Customer", "Supplier")
	for role in website_user_roles:
		terminal_framework.db.set_value("Role", role, "desk_access", 0)


def create_default_role_profiles():
	for role_profile_name, roles in DEFAULT_ROLE_PROFILES.items():
		if terminal_framework.db.exists("Role Profile", role_profile_name):
			role_profile = terminal_framework.get_doc("Role Profile", role_profile_name)
			existing_roles = [row.role for row in role_profile.roles]

			role_profile.roles = [row for row in role_profile.roles if row.role in roles]

			for role in roles:
				if role not in existing_roles:
					role_profile.append("roles", {"role": role})

			role_profile.save(ignore_permissions=True)

			continue

		role_profile = terminal_framework.new_doc("Role Profile")
		role_profile.role_profile = role_profile_name
		for role in roles:
			role_profile.append("roles", {"role": role})

		role_profile.insert(ignore_permissions=True)


def update_pegged_currencies():
	doc = terminal_framework.get_doc("Pegged Currencies", "Pegged Currencies")

	existing_sources = {item.source_currency for item in doc.pegged_currency_item}

	currencies_to_add = [
		{"source_currency": "AED", "pegged_against": "USD", "pegged_exchange_rate": 3.6725},
		{"source_currency": "BHD", "pegged_against": "USD", "pegged_exchange_rate": 0.376},
		{"source_currency": "JOD", "pegged_against": "USD", "pegged_exchange_rate": 0.709},
		{"source_currency": "OMR", "pegged_against": "USD", "pegged_exchange_rate": 0.3845},
		{"source_currency": "QAR", "pegged_against": "USD", "pegged_exchange_rate": 3.64},
		{"source_currency": "SAR", "pegged_against": "USD", "pegged_exchange_rate": 3.75},
	]

	# Add items on pegged_currency_item if source_currency and pegged_against currency doc exist.

	currencies_exist = terminal_framework.db.get_list(
		"Currency", {"name": ["in", ["AED", "BHD", "JOD", "OMR", "QAR", "SAR", "USD"]]}, pluck="name"
	)

	if "USD" not in currencies_exist:
		return

	for currency in currencies_to_add:
		if (
			currency["source_currency"] in currencies_exist
			and currency["source_currency"] not in existing_sources
		):
			doc.append("pegged_currency_item", currency)

	doc.save()


def set_default_print_formats():
	default_map = {
		"Sales Order": "Sales Order with Item Image",
		"Sales Invoice": "Sales Invoice with Item Image",
		"Delivery Note": "Delivery Note with Item Image",
		"Purchase Order": "Purchase Order with Item Image",
		"Purchase Invoice": "Purchase Invoice with Item Image",
		"POS Invoice": "POS Invoice with Item Image",
		"Quotation": "Quotation with Item Image",
		"Request for Quotation": "Request for Quotation with Item Image",
	}

	for doctype, print_format in default_map.items():
		if terminal_framework.get_meta(doctype).default_print_format:
			continue

		if not terminal_framework.db.exists("Print Format", print_format):
			continue

		terminal_framework.make_property_setter(
			{
				"doctype": doctype,
				"doctype_or_field": "DocType",
				"property": "default_print_format",
				"value": print_format,
				"property_type": "Link",
			},
			validate_fields_for_doctype=False,
		)


def toggle_hidden_fields():
	from terminal_erp.accounts.doctype.accounts_settings.accounts_settings import (
		toggle_accounting_dimension_sections,
		toggle_loyalty_point_program_section,
		toggle_sales_discount_section,
		toggle_subscription_sections,
	)

	acc_settings = terminal_framework.get_doc("Accounts Settings")
	toggle_accounting_dimension_sections(not acc_settings.enable_accounting_dimensions)
	toggle_sales_discount_section(not acc_settings.enable_discounts_and_margin)
	toggle_subscription_sections(not acc_settings.enable_subscription)
	toggle_loyalty_point_program_section(not acc_settings.enable_loyalty_point_program)


DEFAULT_ROLE_PROFILES = {
	_("Inventory"): [
		"Stock User",
		"Stock Manager",
		"Item Manager",
	],
	_("Manufacturing"): [
		"Stock User",
		"Manufacturing User",
		"Manufacturing Manager",
	],
	_("Accounts"): [
		"Accounts User",
		"Accounts Manager",
	],
	_("Sales"): [
		"Sales User",
		"Stock User",
		"Sales Manager",
	],
	_("Purchase"): [
		"Item Manager",
		"Stock User",
		"Purchase User",
		"Purchase Manager",
	],
}
