import terminal_framework


def execute():
	terminal_framework.reload_doc("accounts", "doctype", "accounts_settings")

	terminal_framework.db.set_single_value("Accounts Settings", "automatically_process_deferred_accounting_entry", 1)
