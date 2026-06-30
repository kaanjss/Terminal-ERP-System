import terminal_framework
from terminal_framework.query_builder import DocType


def execute():
	if terminal_framework.db.has_column("Asset Repair", "stock_entry"):
		AssetRepair = DocType("Asset Repair")
		StockEntry = DocType("Stock Entry")

		(
			terminal_framework.qb.update(StockEntry)
			.join(AssetRepair)
			.on(StockEntry.name == AssetRepair.stock_entry)
			.set(StockEntry.asset_repair, AssetRepair.name)
		).run()
