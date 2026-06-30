import terminal_framework


def execute():
	if terminal_framework.get_all("Company", filters={"country": "India"}, limit=1):
		terminal_framework.db.set_single_value("Stock Settings", "allow_existing_serial_no", 1)
