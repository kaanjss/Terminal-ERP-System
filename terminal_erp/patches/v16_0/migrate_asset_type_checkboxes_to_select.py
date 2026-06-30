import terminal_framework
from terminal_framework.query_builder import Case


def execute():
	Asset = terminal_framework.qb.DocType("Asset")

	terminal_framework.qb.update(Asset).set(
		Asset.asset_type,
		Case()
		.when(Asset.is_existing_asset == 1, "Existing Asset")
		.when(Asset.is_composite_asset == 1, "Composite Asset")
		.when(Asset.is_composite_component == 1, "Composite Component")
		.else_(""),
	).run()
