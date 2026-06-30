import terminal_framework


def execute():
	terminal_framework.reload_doc("accounts", "doctype", "bank", force=1)

	if (
		terminal_framework.db.table_exists("Bank")
		and terminal_framework.db.table_exists("Bank Account")
		and terminal_framework.db.has_column("Bank Account", "swift_number")
	):
		try:
			terminal_framework.db.sql(
				"""
				UPDATE `tabBank` b, `tabBank Account` ba
				SET b.swift_number = ba.swift_number WHERE b.name = ba.bank
			"""
			)
		except Exception:
			terminal_framework.log_error("Bank to Bank Account patch migration failed")

	terminal_framework.reload_doc("accounts", "doctype", "bank_account")
	terminal_framework.reload_doc("accounts", "doctype", "payment_request")
