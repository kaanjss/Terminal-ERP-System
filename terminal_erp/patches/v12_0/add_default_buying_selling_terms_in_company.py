# Copyright (c) 2019, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	terminal_framework.reload_doc("setup", "doctype", "company")
	if terminal_framework.db.has_column("Company", "default_terms"):
		rename_field("Company", "default_terms", "default_selling_terms")

		for company in terminal_framework.get_all("Company", ["name", "default_selling_terms", "default_buying_terms"]):
			if company.default_selling_terms and not company.default_buying_terms:
				terminal_framework.db.set_value(
					"Company", company.name, "default_buying_terms", company.default_selling_terms
				)

	terminal_framework.reload_doc("setup", "doctype", "terms_and_conditions")
	terminal_framework.db.sql("update `tabTerms and Conditions` set selling=1, buying=1, hr=1")
