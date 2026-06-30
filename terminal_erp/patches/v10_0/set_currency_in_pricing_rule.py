import terminal_framework


def execute():
	terminal_framework.reload_doctype("Pricing Rule")

	currency = terminal_framework.db.get_default("currency")
	for doc in terminal_framework.get_all("Pricing Rule", fields=["company", "name"]):
		if doc.company:
			currency = terminal_framework.get_cached_value("Company", doc.company, "default_currency")

		terminal_framework.db.sql("""update `tabPricing Rule` set currency = %s where name = %s""", (currency, doc.name))
