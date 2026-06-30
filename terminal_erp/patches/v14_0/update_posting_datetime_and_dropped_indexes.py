import terminal_framework


def execute():
	terminal_framework.db.sql(
		"""
		UPDATE `tabStock Ledger Entry`
			SET posting_datetime = DATE_FORMAT(timestamp(posting_date, posting_time), '%Y-%m-%d %H:%i:%s')
	"""
	)

	drop_indexes()


def drop_indexes():
	if not terminal_framework.db.has_index("tabStock Ledger Entry", "posting_sort_index"):
		return

	terminal_framework.db.sql_ddl("ALTER TABLE `tabStock Ledger Entry` DROP INDEX `posting_sort_index`")
