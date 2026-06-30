# Copyright (c) 2019, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("stock", "doctype", "pick_list")
	terminal_framework.db.sql(
		"""UPDATE `tabPick List` set purpose = 'Delivery'
        WHERE docstatus = 1  and purpose = 'Delivery against Sales Order' """
	)
