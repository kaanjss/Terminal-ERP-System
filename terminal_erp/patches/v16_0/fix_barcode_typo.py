import terminal_framework


def execute():
	terminal_framework.qb.update("Item Barcode").set("barcode_type", "EAN-13").where(
		terminal_framework.qb.Field("barcode_type") == "EAN-12"
	).run()
