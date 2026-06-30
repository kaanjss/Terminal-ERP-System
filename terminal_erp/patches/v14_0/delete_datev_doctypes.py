import terminal_framework


def execute():
	install_apps = terminal_framework.get_installed_apps()
	if "terminal_erp_datev_uo" in install_apps or "terminal_erp_datev" in install_apps:
		return

	# doctypes
	terminal_framework.delete_doc("DocType", "DATEV Settings", ignore_missing=True, force=True)

	# reports
	terminal_framework.delete_doc("Report", "DATEV", ignore_missing=True, force=True)
