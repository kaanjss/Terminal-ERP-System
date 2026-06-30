import terminal_framework


def execute():
	warehouses = terminal_framework.get_single_value(
		"Manufacturing Settings",
		["default_wip_warehouse", "default_fg_warehouse", "default_scrap_warehouse"],
		as_dict=True,
	)

	for name, warehouse in warehouses.items():
		if warehouse:
			company = terminal_framework.get_value("Warehouse", warehouse, "company")
			terminal_framework.db.set_value("Company", company, name, warehouse)
