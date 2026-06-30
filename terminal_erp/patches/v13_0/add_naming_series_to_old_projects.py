import terminal_framework


def execute():
	terminal_framework.reload_doc("projects", "doctype", "project")

	terminal_framework.db.sql(
		"""UPDATE `tabProject`
		SET
			naming_series = 'PROJ-.####'
		WHERE
			naming_series is NULL"""
	)
