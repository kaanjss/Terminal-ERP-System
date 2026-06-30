import terminal_framework


def execute():
	stock_closing_entry = terminal_framework.qb.DocType("Stock Closing Entry")
	call_log = terminal_framework.qb.DocType("Call Log")

	# updating stock closing entry status to cancelled from canceled
	(
		terminal_framework.qb.update(stock_closing_entry)
		.set(stock_closing_entry.status, "Cancelled")
		.where(stock_closing_entry.status == "Canceled")
	).run()

	# updating call log status to cancelled from canceled
	(terminal_framework.qb.update(call_log).set(call_log.status, "Cancelled").where(call_log.status == "Canceled")).run()
