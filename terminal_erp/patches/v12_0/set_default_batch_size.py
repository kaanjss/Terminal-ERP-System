import terminal_framework


def execute():
	terminal_framework.reload_doc("manufacturing", "doctype", "bom_operation")
	terminal_framework.reload_doc("manufacturing", "doctype", "work_order_operation")

	terminal_framework.db.sql(
		"""
        UPDATE
            `tabBOM Operation` bo
        SET
            bo.batch_size = 1
    """
	)
	terminal_framework.db.sql(
		"""
        UPDATE
            `tabWork Order Operation` wop
        SET
            wop.batch_size = 1
    """
	)
