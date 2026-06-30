import terminal_framework


def execute():
	for ws in ["Receivables", "Payables"]:
		terminal_framework.delete_doc_if_exists("Workspace Sidebar", ws)
		terminal_framework.delete_doc_if_exists("Workspace", ws)
