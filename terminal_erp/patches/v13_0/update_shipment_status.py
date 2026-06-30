import terminal_framework


def execute():
	terminal_framework.reload_doc("stock", "doctype", "shipment")

	# update submitted status
	terminal_framework.db.sql(
		"""UPDATE `tabShipment`
					SET status = "Submitted"
					WHERE status = "Draft" AND docstatus = 1"""
	)

	# update cancelled status
	terminal_framework.db.sql(
		"""UPDATE `tabShipment`
					SET status = "Cancelled"
					WHERE status = "Draft" AND docstatus = 2"""
	)
