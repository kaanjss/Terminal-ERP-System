import terminal_framework


def execute():
	terminal_framework.reload_doc("setup", "doctype", "uom")

	uom = terminal_framework.qb.DocType("UOM")

	(
		terminal_framework.qb.update(uom)
		.set(uom.enabled, 1)
		.where(uom.creation >= "2021-10-18")  # date when this field was released
	).run()
