import terminal_framework


def execute():
	"""Correct amount in child table of required items table."""

	terminal_framework.reload_doc("manufacturing", "doctype", "work_order")
	terminal_framework.reload_doc("manufacturing", "doctype", "work_order_item")

	terminal_framework.db.sql(
		"""UPDATE `tabWork Order Item` SET amount = ifnull(rate, 0.0) * ifnull(required_qty, 0.0)"""
	)
