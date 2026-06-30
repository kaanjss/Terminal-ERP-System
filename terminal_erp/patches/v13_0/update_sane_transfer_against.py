import terminal_framework


def execute():
	bom = terminal_framework.qb.DocType("BOM")

	(
		terminal_framework.qb.update(bom).set(bom.transfer_material_against, "Work Order").where(bom.with_operations == 0)
	).run()
