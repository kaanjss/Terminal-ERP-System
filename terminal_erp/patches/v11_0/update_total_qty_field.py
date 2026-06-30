import terminal_framework


def execute():
	terminal_framework.reload_doc("buying", "doctype", "purchase_order")
	terminal_framework.reload_doc("buying", "doctype", "supplier_quotation")
	terminal_framework.reload_doc("selling", "doctype", "sales_order")
	terminal_framework.reload_doc("selling", "doctype", "quotation")
	terminal_framework.reload_doc("stock", "doctype", "delivery_note")
	terminal_framework.reload_doc("stock", "doctype", "purchase_receipt")
	terminal_framework.reload_doc("accounts", "doctype", "sales_invoice")
	terminal_framework.reload_doc("accounts", "doctype", "purchase_invoice")

	doctypes = [
		"Sales Order",
		"Sales Invoice",
		"Delivery Note",
		"Purchase Order",
		"Purchase Invoice",
		"Purchase Receipt",
		"Quotation",
		"Supplier Quotation",
	]

	for doctype in doctypes:
		total_qty = terminal_framework.db.sql(
			f"""
			SELECT
				parent, SUM(qty) as qty
			FROM
				`tab{doctype} Item`
			where parenttype = '{doctype}'
			GROUP BY parent
		""",
			as_dict=True,
		)

		# Query to update total_qty might become too big, Update in batches
		# batch_size is chosen arbitrarily, Don't try too hard to reason about it
		batch_size = 100000
		for i in range(0, len(total_qty), batch_size):
			batch_transactions = total_qty[i : i + batch_size]

			# UPDATE with CASE for some reason cannot use PRIMARY INDEX,
			# causing all rows to be examined, leading to a very slow update

			# UPDATE with WHERE clause uses PRIMARY INDEX, but will lead to too many queries

			# INSERT with ON DUPLICATE KEY UPDATE uses PRIMARY INDEX
			# and can perform multiple updates per query
			# This is probably never used anywhere else as of now, but should be
			values = []
			for d in batch_transactions:
				values.append(f"({terminal_framework.db.escape(d.parent)}, {d.qty})")
			conditions = ",".join(values)
			terminal_framework.db.sql(
				f"""
				INSERT INTO `tab{doctype}` (name, total_qty) VALUES {conditions}
				ON DUPLICATE KEY UPDATE name = VALUES(name), total_qty = VALUES(total_qty)
			"""
			)
