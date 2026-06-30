import terminal_framework


def execute():
	if terminal_framework.db.has_table("Tax Withholding Category") and terminal_framework.db.has_column(
		"Tax Withholding Category", "round_off_tax_amount"
	):
		terminal_framework.db.sql(
			"""
			UPDATE `tabTax Withholding Category` set round_off_tax_amount = 0
			WHERE round_off_tax_amount IS NULL
		"""
		)
