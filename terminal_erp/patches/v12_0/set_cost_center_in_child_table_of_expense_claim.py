import terminal_framework


def execute():
	terminal_framework.reload_doc("hr", "doctype", "expense_claim_detail")
	terminal_framework.db.sql(
		"""
		UPDATE `tabExpense Claim Detail` child, `tabExpense Claim` par
		SET child.cost_center = par.cost_center
		WHERE child.parent = par.name
	"""
	)
