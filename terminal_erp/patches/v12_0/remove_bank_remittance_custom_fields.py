import terminal_framework


def execute():
	terminal_framework.reload_doc("accounts", "doctype", "tax_category")
	terminal_framework.reload_doc("stock", "doctype", "item_manufacturer")
	company = terminal_framework.get_all("Company", filters={"country": "India"})
	if not company:
		return
	if terminal_framework.db.exists("Custom Field", "Company-bank_remittance_section"):
		deprecated_fields = [
			"bank_remittance_section",
			"client_code",
			"remittance_column_break",
			"product_code",
		]
		for i in range(len(deprecated_fields)):
			terminal_framework.delete_doc("Custom Field", "Company-" + deprecated_fields[i])
