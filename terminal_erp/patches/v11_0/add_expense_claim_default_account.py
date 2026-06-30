import terminal_framework


def execute():
	terminal_framework.reload_doc("setup", "doctype", "company")

	companies = terminal_framework.get_all("Company", fields=["name", "default_payable_account"])

	for company in companies:
		if company.default_payable_account is not None:
			terminal_framework.db.set_value(
				"Company",
				company.name,
				"default_expense_claim_payable_account",
				company.default_payable_account,
			)
