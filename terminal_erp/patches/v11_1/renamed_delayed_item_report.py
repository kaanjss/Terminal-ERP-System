# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	for report in ["Delayed Order Item Summary", "Delayed Order Summary"]:
		if terminal_framework.db.exists("Report", report):
			terminal_framework.delete_doc("Report", report)
