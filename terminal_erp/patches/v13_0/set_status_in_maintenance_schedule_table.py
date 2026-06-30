import terminal_framework


def execute():
	terminal_framework.reload_doc("maintenance", "doctype", "Maintenance Schedule Detail")
	terminal_framework.db.sql(
		"""
		UPDATE `tabMaintenance Schedule Detail`
		SET completion_status = 'Pending'
		WHERE docstatus < 2
	"""
	)
