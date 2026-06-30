import terminal_framework


def execute():
	Asset = terminal_framework.qb.DocType("Asset")
	query = (
		terminal_framework.qb.update(Asset)
		.set(Asset.status, "Work In Progress")
		.where((Asset.docstatus == 0) & (Asset.is_composite_asset == 1))
	)
	query.run()
