import terminal_framework


def execute():
	doctypes = terminal_framework.get_all("DocType", {"module": "Hub Node", "custom": 0}, pluck="name")
	for doctype in doctypes:
		terminal_framework.delete_doc("DocType", doctype, ignore_missing=True)

	terminal_framework.delete_doc("Module Def", "Hub Node", ignore_missing=True, force=True)
