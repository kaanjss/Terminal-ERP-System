# Copyright(c) 2020, Terminal Framework Technologies Pvt.Ltd.and Contributors
# License: GNU General Public License v3.See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("stock", "doctype", "stock_entry")
	if terminal_framework.db.has_column("Stock Entry", "add_to_transit"):
		terminal_framework.db.sql(
			"""
            UPDATE `tabStock Entry` SET
            stock_entry_type = 'Material Transfer',
            purpose = 'Material Transfer',
            add_to_transit = 1 WHERE stock_entry_type = 'Send to Warehouse'
            """
		)

		terminal_framework.db.sql(
			"""UPDATE `tabStock Entry` SET
            stock_entry_type = 'Material Transfer',
            purpose = 'Material Transfer'
            WHERE stock_entry_type = 'Receive at Warehouse'
            """
		)

		terminal_framework.reload_doc("stock", "doctype", "warehouse_type")
		if not terminal_framework.db.exists("Warehouse Type", "Transit"):
			doc = terminal_framework.new_doc("Warehouse Type")
			doc.name = "Transit"
			doc.insert()

		terminal_framework.reload_doc("stock", "doctype", "stock_entry_type")
		terminal_framework.delete_doc_if_exists("Stock Entry Type", "Send to Warehouse")
		terminal_framework.delete_doc_if_exists("Stock Entry Type", "Receive at Warehouse")
