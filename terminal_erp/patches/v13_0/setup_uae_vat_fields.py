# Copyright (c) 2019, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework

from terminal_erp.regional.united_arab_emirates.setup import setup


def execute():
	company = terminal_framework.get_all("Company", filters={"country": "United Arab Emirates"})
	if not company:
		return

	terminal_framework.reload_doc("regional", "report", "uae_vat_201")
	terminal_framework.reload_doc("regional", "doctype", "uae_vat_settings")
	terminal_framework.reload_doc("regional", "doctype", "uae_vat_account")

	setup()
