# Copyright (c) 2020, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework

from terminal_erp.regional.south_africa.setup import add_permissions, make_custom_fields


def execute():
	company = terminal_framework.get_all("Company", filters={"country": "South Africa"})
	if not company:
		return

	terminal_framework.reload_doc("regional", "doctype", "south_africa_vat_settings")
	terminal_framework.reload_doc("regional", "report", "vat_audit_report")
	terminal_framework.reload_doc("accounts", "doctype", "south_africa_vat_account")

	make_custom_fields()
	add_permissions()
