import terminal_framework


def execute():
	terminal_framework.delete_doc("DocType", "Shopify Settings", ignore_missing=True)
	terminal_framework.delete_doc("DocType", "Shopify Log", ignore_missing=True)
