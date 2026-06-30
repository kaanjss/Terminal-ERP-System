# Copyright (c) 2018, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	"""
	default supplier was not set in the item defaults for multi company instance,
	        this patch will set the default supplier

	"""
	if not terminal_framework.db.has_column("Item", "default_supplier"):
		return

	terminal_framework.reload_doc("stock", "doctype", "item_default")
	terminal_framework.reload_doc("stock", "doctype", "item")

	companies = terminal_framework.get_all("Company")
	if len(companies) > 1:
		terminal_framework.db.sql(
			""" UPDATE `tabItem Default`, `tabItem`
			SET `tabItem Default`.default_supplier = `tabItem`.default_supplier
			WHERE
				`tabItem Default`.parent = `tabItem`.name and `tabItem Default`.default_supplier is null
				and `tabItem`.default_supplier is not null and `tabItem`.default_supplier != '' """
		)
