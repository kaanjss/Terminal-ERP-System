# Copyright (c) 2017, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("setup", "doctype", "party_type")
	party_types = {
		"Customer": "Receivable",
		"Supplier": "Payable",
		"Employee": "Payable",
		"Member": "Receivable",
		"Shareholder": "Payable",
	}

	for party_type, account_type in party_types.items():
		terminal_framework.db.set_value("Party Type", party_type, "account_type", account_type)
