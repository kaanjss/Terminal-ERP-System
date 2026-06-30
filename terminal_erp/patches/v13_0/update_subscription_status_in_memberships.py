import terminal_framework


def execute():
	if terminal_framework.db.exists("DocType", "Member"):
		terminal_framework.reload_doc("Non Profit", "doctype", "Member")

		if terminal_framework.db.has_column("Member", "subscription_activated"):
			terminal_framework.db.sql(
				'UPDATE `tabMember` SET subscription_status = "Active" WHERE subscription_activated = 1'
			)
			terminal_framework.db.sql_ddl("ALTER table `tabMember` DROP COLUMN subscription_activated")
