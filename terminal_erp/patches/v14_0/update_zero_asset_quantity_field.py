import terminal_framework


def execute():
	asset = terminal_framework.qb.DocType("Asset")
	terminal_framework.qb.update(asset).set(asset.asset_quantity, 1).where(asset.asset_quantity == 0).run()
