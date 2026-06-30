import terminal_framework


def execute():
	"""Remove has_variants and attribute fields from item variant settings."""
	terminal_framework.reload_doc("stock", "doctype", "Item Variant Settings")

	terminal_framework.db.sql(
		"""delete from `tabVariant Field`
			where field_name in ('attributes', 'has_variants')"""
	)
