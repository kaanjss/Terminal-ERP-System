# Copyright (c) 2019, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("manufacturing", "doctype", "job_card")
	terminal_framework.reload_doc("manufacturing", "doctype", "job_card_item")
	terminal_framework.reload_doc("manufacturing", "doctype", "work_order_operation")

	terminal_framework.db.sql(
		""" update `tabJob Card` jc, `tabWork Order Operation` wo
		SET	jc.hour_rate =  wo.hour_rate
		WHERE
			jc.operation_id = wo.name and jc.docstatus < 2 and wo.hour_rate > 0
	"""
	)
