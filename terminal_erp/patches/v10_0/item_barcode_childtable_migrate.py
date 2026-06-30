# Copyright (c) 2017, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("stock", "doctype", "item_barcode")
	if terminal_framework.get_all("Item Barcode", limit=1):
		return
	if "barcode" not in terminal_framework.db.get_table_columns("Item"):
		return

	items_barcode = terminal_framework.db.sql("select name, barcode from tabItem where barcode is not null", as_dict=True)
	terminal_framework.reload_doc("stock", "doctype", "item")

	for item in items_barcode:
		barcode = item.barcode.strip()

		if barcode and "<" not in barcode:
			try:
				terminal_framework.get_doc(
					{
						"idx": 0,
						"doctype": "Item Barcode",
						"barcode": barcode,
						"parenttype": "Item",
						"parent": item.name,
						"parentfield": "barcodes",
					}
				).insert()
			except (terminal_framework.DuplicateEntryError, terminal_framework.UniqueValidationError):
				continue
