# Copyright (c) 2020, Terminal Framework Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("accounts", "doctype", "Payment Schedule")
	if terminal_framework.db.count("Payment Schedule"):
		terminal_framework.db.sql(
			"""
			UPDATE
				`tabPayment Schedule` ps
			SET
				ps.outstanding = (ps.payment_amount - ps.paid_amount)
		"""
		)
