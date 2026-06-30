import terminal_framework


def execute():
	terminal_framework.reload_doc("stock", "doctype", "bin")

	terminal_framework.db.sql(
		"""
        UPDATE `tabBin` b
        INNER JOIN `tabWarehouse` w ON b.warehouse = w.name
        SET b.company = w.company
        WHERE b.company IS NULL OR b.company = ''
    """
	)
