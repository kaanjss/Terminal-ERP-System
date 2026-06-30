# Copyright (c) 2018, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	terminal_framework.reload_doc("manufacturing", "doctype", "manufacturing_settings")
	rename_field(
		"Manufacturing Settings",
		"over_production_allowance_percentage",
		"overproduction_percentage_for_sales_order",
	)
