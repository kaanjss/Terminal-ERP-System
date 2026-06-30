import click
import terminal_framework


def execute():
	terminal_framework.db.sql(
		"""
		UPDATE `tabSerial and Batch Bundle`
		JOIN `tabStock Ledger Entry`
		ON `tabSerial and Batch Bundle`.`name` = `tabStock Ledger Entry`.`serial_and_batch_bundle`
		SET `tabSerial and Batch Bundle`.`posting_datetime` = `tabStock Ledger Entry`.`posting_datetime`
		WHERE `tabStock Ledger Entry`.`is_cancelled` = 0
	"""
	)

	drop_indexes()


def drop_indexes():
	table = "tabSerial and Batch Bundle"
	index_list = ["voucher_no_index", "item_code_index", "warehouse_index", "company_index"]

	for index in index_list:
		if not terminal_framework.db.has_index(table, index):
			continue

		try:
			terminal_framework.db.sql_ddl(f"ALTER TABLE `{table}` DROP INDEX `{index}`")
			click.echo(f"✓ dropped {index} index from {table}")
		except Exception:
			terminal_framework.log_error("Failed to drop index")
