# Copyright (c) 2019, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework

from terminal_erp.regional.united_arab_emirates.setup import make_custom_fields


def execute():
	company = terminal_framework.get_all("Company", filters={"country": ["in", ["Saudi Arabia", "United Arab Emirates"]]})
	if not company:
		return

	terminal_framework.reload_doc("accounts", "doctype", "pos_invoice")
	terminal_framework.reload_doc("accounts", "doctype", "pos_invoice_item")

	make_custom_fields()
