import terminal_framework


def execute():
	terminal_framework.reload_doc("custom", "doctype", "custom_field", force=True)
	company = terminal_framework.get_all("Company", filters={"country": "India"})
	if not company:
		return

	if terminal_framework.db.exists("Custom Field", {"fieldname": "vehicle_no"}):
		terminal_framework.db.set_value("Custom Field", {"fieldname": "vehicle_no"}, "mandatory_depends_on", "")
