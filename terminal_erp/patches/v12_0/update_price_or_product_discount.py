import terminal_framework


def execute():
	terminal_framework.reload_doc("accounts", "doctype", "pricing_rule")

	terminal_framework.db.sql(
		""" UPDATE `tabPricing Rule` SET price_or_product_discount = 'Price'
		WHERE ifnull(price_or_product_discount,'') = '' """
	)
