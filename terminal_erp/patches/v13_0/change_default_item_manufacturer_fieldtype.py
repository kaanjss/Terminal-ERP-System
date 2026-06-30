import terminal_framework


def execute():
	# Erase all default item manufacturers that dont exist.
	item = terminal_framework.qb.DocType("Item")
	manufacturer = terminal_framework.qb.DocType("Manufacturer")

	(
		terminal_framework.qb.update(item)
		.set(item.default_item_manufacturer, None)
		.left_join(manufacturer)
		.on(item.default_item_manufacturer == manufacturer.name)
		.where(manufacturer.name.isnull() & item.default_item_manufacturer.isnotnull())
	).run()
