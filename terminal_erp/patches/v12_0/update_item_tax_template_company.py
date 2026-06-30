import terminal_framework


def execute():
	terminal_framework.reload_doc("accounts", "doctype", "item_tax_template")

	item_tax_template_list = terminal_framework.get_list("Item Tax Template")
	for template in item_tax_template_list:
		doc = terminal_framework.get_doc("Item Tax Template", template.name)
		for tax in doc.taxes:
			doc.company = terminal_framework.get_value("Account", tax.tax_type, "company")
			break
		doc.save()
