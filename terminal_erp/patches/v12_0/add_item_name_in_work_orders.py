import terminal_framework


def execute():
	terminal_framework.reload_doc("manufacturing", "doctype", "work_order")

	terminal_framework.db.sql(
		"""
		UPDATE
			`tabWork Order` wo
				JOIN `tabItem` item ON wo.production_item = item.item_code
		SET
			wo.item_name = item.item_name
	"""
	)
	terminal_framework.db.commit()
