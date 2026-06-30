import terminal_framework


def execute():
	if not terminal_framework.db.get_single_value("POS Settings", "invoice_type"):
		terminal_framework.db.set_single_value("POS Settings", "invoice_type", "POS Invoice")
