# Copyright (c) 2023, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import terminal_framework

from terminal_erp import get_default_company


def execute():
	company = get_default_company()
	if company:
		for d in terminal_framework.get_all("Lower Deduction Certificate", pluck="name"):
			terminal_framework.db.set_value("Lower Deduction Certificate", d, "company", company, update_modified=False)
