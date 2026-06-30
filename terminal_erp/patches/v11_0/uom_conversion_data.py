import terminal_framework


def execute():
	from terminal_erp.setup.setup_wizard.operations.install_fixtures import add_uom_data

	terminal_framework.reload_doc("setup", "doctype", "UOM Conversion Factor")
	terminal_framework.reload_doc("setup", "doctype", "UOM")
	terminal_framework.reload_doc("stock", "doctype", "UOM Category")

	if not terminal_framework.db.a_row_exists("UOM Conversion Factor"):
		add_uom_data()
	else:
		# delete conversion data and insert again
		terminal_framework.db.sql("delete from `tabUOM Conversion Factor`")
		try:
			terminal_framework.delete_doc("UOM", "Hundredweight")
			terminal_framework.delete_doc("UOM", "Pound Cubic Yard")
		except terminal_framework.LinkExistsError:
			pass

		add_uom_data()
