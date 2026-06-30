import terminal_framework


def execute():
	terminal_framework.reload_doc("stock", "doctype", "item_variant_attribute")
	terminal_framework.db.sql(
		"""
		UPDATE `tabItem Variant Attribute` t1
		INNER JOIN `tabItem` t2 ON t2.name = t1.parent
		SET t1.variant_of = t2.variant_of
	"""
	)
