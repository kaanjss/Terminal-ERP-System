import terminal_framework


def execute():
	for stock_entry_type in [
		"Receive from Customer",
		"Return Raw Material to Customer",
		"Subcontracting Delivery",
		"Subcontracting Return",
	]:
		if not terminal_framework.db.exists("Stock Entry Type", stock_entry_type):
			terminal_framework.new_doc("Stock Entry Type", purpose=stock_entry_type, is_standard=1).insert(
				set_name=stock_entry_type, ignore_permissions=True
			)
