import terminal_framework


def execute():
	if terminal_framework.db.count("Asset"):
		terminal_framework.reload_doc("assets", "doctype", "Asset")
		asset = terminal_framework.qb.DocType("Asset")
		terminal_framework.qb.update(asset).set(asset.asset_quantity, 1).run()
