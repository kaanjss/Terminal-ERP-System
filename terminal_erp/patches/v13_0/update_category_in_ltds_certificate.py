import terminal_framework


def execute():
	company = terminal_framework.get_all("Company", filters={"country": "India"})
	if not company:
		return

	terminal_framework.reload_doc("regional", "doctype", "lower_deduction_certificate")

	ldc = terminal_framework.qb.DocType("Lower Deduction Certificate").as_("ldc")
	supplier = terminal_framework.qb.DocType("Supplier")

	terminal_framework.qb.update(ldc).inner_join(supplier).on(ldc.supplier == supplier.name).set(
		ldc.tax_withholding_category, supplier.tax_withholding_category
	).where(ldc.tax_withholding_category.isnull()).run()
