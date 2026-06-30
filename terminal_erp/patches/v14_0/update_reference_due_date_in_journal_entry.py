import terminal_framework


def execute():
	if terminal_framework.db.get_value("Journal Entry Account", {"reference_due_date": ""}):
		terminal_framework.db.sql(
			"""
			UPDATE `tabJournal Entry Account`
			SET reference_due_date = NULL
			WHERE reference_due_date = ''
		"""
		)
