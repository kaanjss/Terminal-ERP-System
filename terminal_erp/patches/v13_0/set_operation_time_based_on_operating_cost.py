import terminal_framework


def execute():
	terminal_framework.reload_doc("manufacturing", "doctype", "bom")
	terminal_framework.reload_doc("manufacturing", "doctype", "bom_operation")

	terminal_framework.db.sql(
		"""
		UPDATE
			`tabBOM Operation`
		SET
			time_in_mins = (operating_cost * 60) / hour_rate
		WHERE
			time_in_mins = 0 AND operating_cost > 0
			AND hour_rate > 0 AND docstatus = 1 AND parenttype = "BOM"
	"""
	)
