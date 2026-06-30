import terminal_framework


def execute():
	terminal_framework.reload_doc("selling", "doctype", "sales_order_item", force=True)
	terminal_framework.reload_doc("buying", "doctype", "purchase_order_item", force=True)

	for doctype in ("Sales Order Item", "Purchase Order Item"):
		terminal_framework.db.sql(
			f"""
			UPDATE `tab{doctype}`
			SET against_blanket_order = 1
			WHERE ifnull(blanket_order, '') != ''
		"""
		)
