import terminal_framework


def execute():
	pos_invoice_merge_logs = terminal_framework.db.get_all(
		"POS Invoice Merge Log", {"docstatus": 1}, ["name", "pos_closing_entry"]
	)

	terminal_framework.db.auto_commit_on_many_writes = 1
	for log in pos_invoice_merge_logs:
		if log.pos_closing_entry and terminal_framework.db.exists("POS Closing Entry", log.pos_closing_entry):
			company = terminal_framework.db.get_value("POS Closing Entry", log.pos_closing_entry, "company")
			terminal_framework.db.set_value("POS Invoice Merge Log", log.name, "company", company)

	terminal_framework.db.auto_commit_on_many_writes = 0
