import terminal_framework


def execute():
	terminal_framework.reload_doc("manufacturing", "doctype", "workstation")

	terminal_framework.db.sql(
		""" UPDATE `tabWorkstation`
        SET production_capacity = 1 """
	)
