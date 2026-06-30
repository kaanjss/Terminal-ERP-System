import terminal_framework


def execute():
	for ws in ["Retail", "Utilities"]:
		terminal_framework.delete_doc_if_exists("Workspace", ws)

	for ws in ["Integrations", "Settings"]:
		terminal_framework.db.set_value("Workspace", ws, "public", 0)
