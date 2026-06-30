import terminal_framework


def execute():
	for gateway_account in terminal_framework.get_list("Payment Gateway Account", fields=["name", "payment_account"]):
		company = terminal_framework.db.get_value("Account", gateway_account.payment_account, "company")
		terminal_framework.db.set_value("Payment Gateway Account", gateway_account.name, "company", company)
