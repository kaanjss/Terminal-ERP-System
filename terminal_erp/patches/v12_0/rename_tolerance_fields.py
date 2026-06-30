import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	terminal_framework.reload_doc("stock", "doctype", "item")
	terminal_framework.reload_doc("stock", "doctype", "stock_settings")
	terminal_framework.reload_doc("accounts", "doctype", "accounts_settings")

	rename_field("Stock Settings", "tolerance", "over_delivery_receipt_allowance")
	rename_field("Item", "tolerance", "over_delivery_receipt_allowance")

	qty_allowance = terminal_framework.db.get_single_value("Stock Settings", "over_delivery_receipt_allowance")
	terminal_framework.db.set_single_value("Accounts Settings", "over_delivery_receipt_allowance", qty_allowance)

	terminal_framework.db.sql("update tabItem set over_billing_allowance=over_delivery_receipt_allowance")
