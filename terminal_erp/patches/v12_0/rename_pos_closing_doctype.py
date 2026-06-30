# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	if terminal_framework.db.table_exists("POS Closing Voucher"):
		if not terminal_framework.db.exists("DocType", "POS Closing Entry"):
			terminal_framework.rename_doc("DocType", "POS Closing Voucher", "POS Closing Entry", force=True)

		if not terminal_framework.db.exists("DocType", "POS Closing Entry Taxes"):
			terminal_framework.rename_doc("DocType", "POS Closing Voucher Taxes", "POS Closing Entry Taxes", force=True)

		if not terminal_framework.db.exists("DocType", "POS Closing Voucher Details"):
			terminal_framework.rename_doc(
				"DocType", "POS Closing Voucher Details", "POS Closing Entry Detail", force=True
			)

		terminal_framework.reload_doc("Accounts", "doctype", "POS Closing Entry")
		terminal_framework.reload_doc("Accounts", "doctype", "POS Closing Entry Taxes")
		terminal_framework.reload_doc("Accounts", "doctype", "POS Closing Entry Detail")

	if terminal_framework.db.exists("DocType", "POS Closing Voucher"):
		terminal_framework.delete_doc("DocType", "POS Closing Voucher")
		terminal_framework.delete_doc("DocType", "POS Closing Voucher Taxes")
		terminal_framework.delete_doc("DocType", "POS Closing Voucher Details")
		terminal_framework.delete_doc("DocType", "POS Closing Voucher Invoices")
