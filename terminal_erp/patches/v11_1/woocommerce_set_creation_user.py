import terminal_framework
from terminal_framework.utils import cint


def execute():
	terminal_framework.reload_doc("terminal_erp_integrations", "doctype", "woocommerce_settings")
	doc = terminal_framework.get_doc("Woocommerce Settings")

	if cint(doc.enable_sync):
		doc.creation_user = doc.modified_by
		doc.save(ignore_permissions=True)
