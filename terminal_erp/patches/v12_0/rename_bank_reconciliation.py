# Copyright (c) 2018, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	if terminal_framework.db.table_exists("Bank Reconciliation"):
		terminal_framework.rename_doc("DocType", "Bank Reconciliation", "Bank Clearance", force=True)
		terminal_framework.reload_doc("Accounts", "doctype", "Bank Clearance")

		terminal_framework.rename_doc("DocType", "Bank Reconciliation Detail", "Bank Clearance Detail", force=True)
		terminal_framework.reload_doc("Accounts", "doctype", "Bank Clearance Detail")
