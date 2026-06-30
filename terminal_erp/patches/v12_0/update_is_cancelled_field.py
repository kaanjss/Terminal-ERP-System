import terminal_framework


def execute():
	# handle type casting for is_cancelled field
	module_doctypes = (
		("stock", "Stock Ledger Entry"),
		("stock", "Serial No"),
		("accounts", "GL Entry"),
	)

	for module, doctype in module_doctypes:
		if (
			not terminal_framework.db.has_column(doctype, "is_cancelled")
			or terminal_framework.db.get_column_type(doctype, "is_cancelled").lower() == "int(1)"
		):
			continue

		terminal_framework.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_cancelled = 0
				where is_cancelled in ('', 'No') or is_cancelled is NULL"""
		)
		terminal_framework.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_cancelled = 1
				where is_cancelled = 'Yes'"""
		)

		terminal_framework.reload_doc(module, "doctype", terminal_framework.scrub(doctype))
