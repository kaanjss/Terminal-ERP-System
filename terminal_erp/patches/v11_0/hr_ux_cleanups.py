import terminal_framework


def execute():
	terminal_framework.reload_doctype("Employee")
	terminal_framework.db.sql("update tabEmployee set first_name = employee_name")

	# update holiday list
	terminal_framework.reload_doctype("Holiday List")
	for holiday_list in terminal_framework.get_all("Holiday List"):
		holiday_list = terminal_framework.get_doc("Holiday List", holiday_list.name)
		holiday_list.db_set("total_holidays", len(holiday_list.holidays), update_modified=False)
