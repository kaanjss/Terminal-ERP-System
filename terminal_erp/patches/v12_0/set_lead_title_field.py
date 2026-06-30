import terminal_framework


def execute():
	terminal_framework.reload_doc("crm", "doctype", "lead")
	terminal_framework.db.sql(
		"""
		UPDATE
			`tabLead`
		SET
			title = IF(organization_lead = 1, company_name, lead_name)
	"""
	)
