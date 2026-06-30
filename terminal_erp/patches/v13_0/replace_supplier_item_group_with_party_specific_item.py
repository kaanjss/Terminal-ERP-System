# Copyright (c) 2019, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework


def execute():
	if terminal_framework.db.table_exists("Supplier Item Group"):
		terminal_framework.reload_doc("selling", "doctype", "party_specific_item")
		sig = terminal_framework.db.get_all("Supplier Item Group", fields=["name", "supplier", "item_group"])
		for item in sig:
			psi = terminal_framework.new_doc("Party Specific Item")
			psi.party_type = "Supplier"
			psi.party = item.supplier
			psi.restrict_based_on = "Item Group"
			psi.based_on_value = item.item_group
			psi.insert()
