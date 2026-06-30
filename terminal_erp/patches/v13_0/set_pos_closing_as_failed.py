import terminal_framework


def execute():
	terminal_framework.reload_doc("accounts", "doctype", "pos_closing_entry")

	terminal_framework.db.sql("update `tabPOS Closing Entry` set `status` = 'Failed' where `status` = 'Queued'")
