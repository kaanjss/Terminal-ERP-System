import terminal_framework


def execute():
	if terminal_framework.db.exists("DocType", "Membership"):
		if "webhook_payload" in terminal_framework.db.get_table_columns("Membership"):
			terminal_framework.db.sql("alter table `tabMembership` drop column webhook_payload")
