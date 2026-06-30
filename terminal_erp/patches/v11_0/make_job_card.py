# Copyright (c) 2017, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework

from terminal_erp.manufacturing.doctype.work_order.work_order import create_job_card


def execute():
	terminal_framework.reload_doc("manufacturing", "doctype", "work_order")
	terminal_framework.reload_doc("manufacturing", "doctype", "work_order_item")
	terminal_framework.reload_doc("manufacturing", "doctype", "job_card")
	terminal_framework.reload_doc("manufacturing", "doctype", "job_card_item")

	fieldname = terminal_framework.db.get_value(
		"DocField", {"fieldname": "work_order", "parent": "Timesheet"}, "fieldname"
	)
	if not fieldname:
		fieldname = terminal_framework.db.get_value(
			"DocField", {"fieldname": "production_order", "parent": "Timesheet"}, "fieldname"
		)
		if not fieldname:
			return

	for d in terminal_framework.get_all(
		"Timesheet", filters={fieldname: ["!=", ""], "docstatus": 0}, fields=[fieldname, "name"]
	):
		if d[fieldname]:
			doc = terminal_framework.get_doc("Work Order", d[fieldname])
			for row in doc.operations:
				create_job_card(doc, row, auto_create=True)
			terminal_framework.delete_doc("Timesheet", d.name)
