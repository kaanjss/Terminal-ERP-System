import terminal_framework


def execute():
	doctype = "Stock Reconciliation Item"

	if not terminal_framework.db.has_column(doctype, "current_serial_no"):
		# nothing to fix if column doesn't exist
		return

	sr_item = terminal_framework.qb.DocType(doctype)

	(terminal_framework.qb.update(sr_item).set(sr_item.current_serial_no, None).where(sr_item.current_qty == 0)).run()
