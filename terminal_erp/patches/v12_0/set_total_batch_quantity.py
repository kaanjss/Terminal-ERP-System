import terminal_framework


def execute():
	terminal_framework.reload_doc("stock", "doctype", "batch")

	for batch in terminal_framework.get_all("Batch", fields=["name", "batch_id"]):
		batch_qty = (
			terminal_framework.db.get_value(
				"Stock Ledger Entry",
				{"docstatus": 1, "batch_no": batch.batch_id, "is_cancelled": 0},
				[{"SUM": "actual_qty"}],
			)
			or 0.0
		)
		terminal_framework.db.set_value("Batch", batch.name, "batch_qty", batch_qty, update_modified=False)
