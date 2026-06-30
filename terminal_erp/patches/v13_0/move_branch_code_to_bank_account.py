# Copyright (c) 2019, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("accounts", "doctype", "bank_account")
	terminal_framework.reload_doc("accounts", "doctype", "bank")

	if terminal_framework.db.has_column("Bank", "branch_code") and terminal_framework.db.has_column("Bank Account", "branch_code"):
		terminal_framework.db.sql(
			"""UPDATE `tabBank` b, `tabBank Account` ba
			SET ba.branch_code = b.branch_code
			WHERE ba.bank = b.name AND
			ifnull(b.branch_code, '') != '' AND ifnull(ba.branch_code, '') = ''"""
		)
