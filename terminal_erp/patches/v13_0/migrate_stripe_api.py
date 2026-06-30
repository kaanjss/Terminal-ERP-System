import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	terminal_framework.reload_doc("accounts", "doctype", "subscription_plan")
	rename_field("Subscription Plan", "payment_plan_id", "product_price_id")
