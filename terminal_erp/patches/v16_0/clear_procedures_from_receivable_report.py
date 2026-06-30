import terminal_framework


def execute():
	terminal_framework.db.sql("drop function if exists ar_genkey")
	terminal_framework.db.sql("drop procedure if exists ar_init_tmp_table")
	terminal_framework.db.sql("drop procedure if exists ar_allocate_to_tmp_table")

	if terminal_framework.db.get_single_value("Accounts Settings", "receivable_payable_fetch_method") == "Raw SQL":
		terminal_framework.db.set_single_value(
			"Accounts Settings", "receivable_payable_fetch_method", "UnBuffered Cursor"
		)
