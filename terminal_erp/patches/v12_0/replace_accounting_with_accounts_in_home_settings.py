import terminal_framework


def execute():
	terminal_framework.db.sql(
		"""UPDATE `tabUser` SET `home_settings` = REPLACE(`home_settings`, 'Accounting', 'Accounts')"""
	)
	terminal_framework.cache().delete_key("home_settings")
