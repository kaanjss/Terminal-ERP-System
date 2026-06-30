import terminal_framework


def execute():
	if "agriculture" in terminal_framework.get_installed_apps():
		return

	for role in ["Agriculture User", "Agriculture Manager"]:
		assignments = terminal_framework.get_all("Has Role", {"role": role}, pluck="name")
		for assignment in assignments:
			terminal_framework.delete_doc("Has Role", assignment, ignore_missing=True, force=True)
		terminal_framework.delete_doc("Role", role, ignore_missing=True, force=True)
