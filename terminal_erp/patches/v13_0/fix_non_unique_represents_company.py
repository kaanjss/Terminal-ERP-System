import terminal_framework


def execute():
	terminal_framework.db.sql(
		"""
		update tabCustomer
		set represents_company = NULL
		where represents_company = ''
	"""
	)
