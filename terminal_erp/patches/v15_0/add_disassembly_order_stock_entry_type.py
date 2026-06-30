import terminal_framework


def execute():
	if not terminal_framework.db.exists("Stock Entry Type", "Disassemble"):
		terminal_framework.get_doc(
			{
				"doctype": "Stock Entry Type",
				"name": "Disassemble",
				"purpose": "Disassemble",
				"is_standard": 1,
			}
		).insert(ignore_permissions=True)
