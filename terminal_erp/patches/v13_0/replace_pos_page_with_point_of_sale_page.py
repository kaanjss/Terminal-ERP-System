import terminal_framework


def execute():
	if terminal_framework.db.exists("Page", "point-of-sale"):
		terminal_framework.rename_doc("Page", "pos", "point-of-sale", 1, 1)
