import terminal_framework


# not able to use terminal_framework.qb because of this bug https://github.com/terminal_framework/terminal_framework/issues/20292
def execute():
	if terminal_framework.db.has_column("Asset Repair", "warehouse"):
		# nosemgrep
		terminal_framework.db.sql(
			"""UPDATE `tabAsset Repair Consumed Item` ar_item
			JOIN `tabAsset Repair` ar
			ON ar.name = ar_item.parent
			SET ar_item.warehouse = ar.warehouse
			WHERE ifnull(ar.warehouse, '') != ''"""
		)
