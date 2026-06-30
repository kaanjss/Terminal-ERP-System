import terminal_framework


def execute():
	from terminal_erp.setup.setup_wizard.operations.install_fixtures import add_uom_data

	terminal_framework.reload_doc("setup", "doctype", "UOM Conversion Factor")
	terminal_framework.reload_doc("setup", "doctype", "UOM")
	terminal_framework.reload_doc("stock", "doctype", "UOM Category")

	add_uom_data()
