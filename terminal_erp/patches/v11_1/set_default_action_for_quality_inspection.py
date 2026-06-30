# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	stock_settings = terminal_framework.get_doc("Stock Settings")
	if stock_settings.default_warehouse and not terminal_framework.db.exists(
		"Warehouse", stock_settings.default_warehouse
	):
		stock_settings.default_warehouse = None
	if stock_settings.stock_uom and not terminal_framework.db.exists("UOM", stock_settings.stock_uom):
		stock_settings.stock_uom = None
	stock_settings.flags.ignore_mandatory = True
	stock_settings.action_if_quality_inspection_is_not_submitted = "Stop"
	stock_settings.save()
