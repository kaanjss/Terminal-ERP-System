import terminal_framework


def execute():
	terminal_framework.db.sql(
		"""
		UPDATE `tabStock Ledger Entry`
			SET posting_datetime = timestamp(posting_date, posting_time)
	"""
	)
