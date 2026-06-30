# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt"


import terminal_framework
from terminal_framework.defaults import get_user_default
from terminal_framework.utils import cint

import terminal_erp.accounts.utils


def boot_session(bootinfo):
	"""boot session - send website info if guest"""

	if terminal_framework.session["user"] != "Guest":
		update_page_info(bootinfo)

		bootinfo.sysdefaults.territory = terminal_framework.get_single_value("Selling Settings", "territory")
		bootinfo.sysdefaults.customer_group = terminal_framework.get_single_value("Selling Settings", "customer_group")
		bootinfo.sysdefaults.use_legacy_js_reactivity = cint(
			terminal_framework.get_single_value("Selling Settings", "use_legacy_js_reactivity")
		)
		bootinfo.sysdefaults.allow_stale = cint(terminal_framework.get_single_value("Accounts Settings", "allow_stale"))
		bootinfo.sysdefaults.over_billing_allowance = terminal_framework.get_single_value(
			"Accounts Settings", "over_billing_allowance"
		)

		bootinfo.sysdefaults.quotation_valid_till = cint(
			terminal_framework.db.get_single_value("CRM Settings", "default_valid_till")
		)

		bootinfo.sysdefaults.allow_sales_order_creation_for_expired_quotation = cint(
			terminal_framework.get_single_value("Selling Settings", "allow_sales_order_creation_for_expired_quotation")
		)

		# if no company, show a dialog box to create a new company
		bootinfo.customer_count = terminal_framework.db.count("Customer")

		if not bootinfo.customer_count:
			bootinfo.setup_complete = "Yes" if terminal_framework.db.get_all("Company", limit=1) else "No"

		companies = terminal_framework.get_all(
			"Company",
			fields=[
				"name",
				"default_currency",
				"cost_center",
				"default_selling_terms",
				"default_buying_terms",
				"default_letter_head",
				"default_letter_head_report",
				"default_bank_account",
				"enable_perpetual_inventory",
				"country",
				"exchange_gain_loss_account",
			],
			limit_page_length=0,  # intentionally unbounded: all companies are needed for boot
		)
		for company in companies:
			company.doctype = ":Company"
		bootinfo.docs += companies

		party_account_types = terminal_framework.get_all("Party Type", fields=["name", "account_type"], as_list=True)
		bootinfo.party_account_types = terminal_framework._dict(
			(name, account_type or "") for name, account_type in party_account_types
		)
		fiscal_year = terminal_erp.accounts.utils.get_fiscal_years(
			terminal_framework.utils.nowdate(), company=get_user_default("company"), raise_on_missing=False
		)
		if fiscal_year:
			bootinfo.current_fiscal_year = fiscal_year[0]

		bootinfo.sysdefaults.demo_company = terminal_framework.db.get_single_value("Global Defaults", "demo_company")
		bootinfo.sysdefaults.default_ageing_range = terminal_framework.db.get_single_value(
			"Accounts Settings", "default_ageing_range"
		)
		bootinfo.sysdefaults.repost_allowed_doctypes = terminal_framework.get_hooks("repost_allowed_doctypes")


def update_page_info(bootinfo):
	bootinfo.page_info.update(
		{
			"Chart of Accounts": {"title": "Chart of Accounts", "route": "Tree/Account"},
			"Chart of Cost Centers": {"title": "Chart of Cost Centers", "route": "Tree/Cost Center"},
			"Item Group Tree": {"title": "Item Group Tree", "route": "Tree/Item Group"},
			"Customer Group Tree": {"title": "Customer Group Tree", "route": "Tree/Customer Group"},
			"Territory Tree": {"title": "Territory Tree", "route": "Tree/Territory"},
			"Sales Person Tree": {"title": "Sales Person Tree", "route": "Tree/Sales Person"},
		}
	)


def bootinfo(bootinfo):
	if bootinfo.get("user") and bootinfo["user"].get("name"):
		bootinfo["user"]["employee"] = ""
		terminal_framework.session.data.employee = ""
		employee = terminal_framework.db.get_value("Employee", {"user_id": bootinfo["user"]["name"]}, "name")
		if employee:
			bootinfo["user"]["employee"] = employee
			terminal_framework.session.data.employee = employee
