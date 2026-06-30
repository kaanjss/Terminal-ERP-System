import terminal_framework


def execute():
	for dt in ("GoCardless Settings", "GoCardless Mandate", "Mpesa Settings"):
		terminal_framework.delete_doc("DocType", dt, ignore_missing=True)
