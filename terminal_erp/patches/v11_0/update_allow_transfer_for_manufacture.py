# Copyright (c) 2018, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("stock", "doctype", "item")
	terminal_framework.db.sql(
		""" update `tabItem` set include_item_in_manufacturing = 1
		where ifnull(is_stock_item, 0) = 1"""
	)

	for doctype in ["BOM Item", "Work Order Item", "BOM Explosion Item"]:
		terminal_framework.reload_doc("manufacturing", "doctype", terminal_framework.scrub(doctype))

		terminal_framework.db.sql(
			f""" update `tab{doctype}` child, tabItem item
			set
				child.include_item_in_manufacturing = 1
			where
				child.item_code = item.name and ifnull(item.is_stock_item, 0) = 1
		"""
		)
