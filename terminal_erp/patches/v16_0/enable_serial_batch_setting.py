import terminal_framework


def execute():
	if not terminal_framework.get_all("Serial No", limit=1) and not terminal_framework.get_all("Batch", limit=1):
		return

	terminal_framework.db.set_single_value("Stock Settings", "enable_serial_and_batch_no_for_item", 1)
	terminal_framework.db.set_default("enable_serial_and_batch_no_for_item", 1)
