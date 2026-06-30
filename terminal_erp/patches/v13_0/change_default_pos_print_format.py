import terminal_framework


def execute():
	terminal_framework.db.sql(
		"""UPDATE `tabPOS Profile` profile
		SET profile.`print_format` = 'POS Invoice'
		WHERE profile.`print_format` = 'Point of Sale'"""
	)
