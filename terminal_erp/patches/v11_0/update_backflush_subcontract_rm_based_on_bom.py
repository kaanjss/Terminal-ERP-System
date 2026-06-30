# Copyright (c) 2017, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("buying", "doctype", "buying_settings")
	terminal_framework.db.set_single_value("Buying Settings", "backflush_raw_materials_of_subcontract_based_on", "BOM")

	terminal_framework.reload_doc("stock", "doctype", "stock_entry_detail")
	terminal_framework.db.sql(
		""" update `tabStock Entry Detail` as sed,
		`tabStock Entry` as se, `tabPurchase Order Item Supplied` as pois
		set
			sed.subcontracted_item = pois.main_item_code
		where
			se.purpose = 'Send to Subcontractor' and sed.parent = se.name
			and pois.rm_item_code = sed.item_code and se.docstatus = 1
			and pois.parenttype = 'Purchase Order'"""
	)
