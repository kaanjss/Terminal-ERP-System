import terminal_framework


def execute():
	valuation_method = terminal_framework.db.get_single_value("Stock Settings", "valuation_method")
	if valuation_method in ["FIFO", "LIFO"]:
		return

	if terminal_framework.get_all("Batch", filters={"use_batchwise_valuation": 1}, limit=1):
		return

	if terminal_framework.get_all("Item", filters={"has_batch_no": 1, "valuation_method": "FIFO"}, limit=1):
		return

	terminal_framework.db.set_single_value("Stock Settings", "do_not_use_batchwise_valuation", 1)
