import terminal_framework


def execute():
	sabb = terminal_framework.get_all("Serial and Batch Bundle", filters={"docstatus": ("<", 2)}, limit=1)
	if not sabb:
		terminal_framework.db.set_single_value("Stock Settings", "use_serial_batch_fields", 1)
