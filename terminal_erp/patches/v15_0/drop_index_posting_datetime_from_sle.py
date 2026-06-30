import click
import terminal_framework


def execute():
	table = "tabStock Ledger Entry"
	index = "posting_datetime_creation_index"

	if not terminal_framework.db.has_index(table, index):
		return

	try:
		terminal_framework.db.sql_ddl(f"ALTER TABLE `{table}` DROP INDEX `{index}`")
		click.echo(f"✓ dropped {index} index from {table}")
	except Exception:
		terminal_framework.log_error("Failed to drop index")
