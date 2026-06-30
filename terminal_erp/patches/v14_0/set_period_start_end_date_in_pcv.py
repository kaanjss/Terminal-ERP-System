# Copyright (c) 2023, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import terminal_framework


def execute():
	# nosemgrep
	terminal_framework.db.sql(
		"""
		UPDATE `tabPeriod Closing Voucher`
		SET
			period_start_date = (select year_start_date from `tabFiscal Year` where name = fiscal_year),
			period_end_date = posting_date
	"""
	)
