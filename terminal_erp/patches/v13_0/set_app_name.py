import terminal_framework


def execute():
	terminal_framework.reload_doctype("System Settings")
	settings = terminal_framework.get_doc("System Settings")
	settings.db_set("app_name", "Terminal ERP", commit=True)
