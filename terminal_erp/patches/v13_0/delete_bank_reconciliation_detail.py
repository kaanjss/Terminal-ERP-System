# Copyright (c) 2019, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	if terminal_framework.db.exists("DocType", "Bank Reconciliation Detail") and terminal_framework.db.exists(
		"DocType", "Bank Clearance Detail"
	):
		terminal_framework.delete_doc("DocType", "Bank Reconciliation Detail", force=1)
