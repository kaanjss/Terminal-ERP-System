import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	terminal_framework.reload_doc("assets", "doctype", "asset")
	if terminal_framework.db.has_column("Asset", "purchase_receipt_amount"):
		rename_field("Asset", "purchase_receipt_amount", "purchase_amount")
