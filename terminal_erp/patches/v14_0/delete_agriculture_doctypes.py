import terminal_framework


def execute():
	if "agriculture" in terminal_framework.get_installed_apps():
		return

	terminal_framework.delete_doc("Module Def", "Agriculture", ignore_missing=True, force=True)

	terminal_framework.delete_doc("Workspace", "Agriculture", ignore_missing=True, force=True)

	reports = terminal_framework.get_all("Report", {"module": "agriculture", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		terminal_framework.delete_doc("Report", report, ignore_missing=True, force=True)

	dashboards = terminal_framework.get_all("Dashboard", {"module": "agriculture", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		terminal_framework.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	doctypes = terminal_framework.get_all("DocType", {"module": "agriculture", "custom": 0}, pluck="name")
	for doctype in doctypes:
		terminal_framework.delete_doc("DocType", doctype, ignore_missing=True)

	terminal_framework.delete_doc("Module Def", "Agriculture", ignore_missing=True, force=True)
