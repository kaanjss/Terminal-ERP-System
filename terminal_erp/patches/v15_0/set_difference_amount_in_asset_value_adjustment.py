import terminal_framework


def execute():
	AssetValueAdjustment = terminal_framework.qb.DocType("Asset Value Adjustment")

	terminal_framework.qb.update(AssetValueAdjustment).set(
		AssetValueAdjustment.difference_amount,
		AssetValueAdjustment.new_asset_value - AssetValueAdjustment.current_asset_value,
	).where(AssetValueAdjustment.docstatus != 2).run()
