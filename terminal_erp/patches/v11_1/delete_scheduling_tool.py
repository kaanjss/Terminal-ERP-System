# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	if terminal_framework.db.exists("DocType", "Scheduling Tool"):
		terminal_framework.delete_doc("DocType", "Scheduling Tool", ignore_permissions=True)
