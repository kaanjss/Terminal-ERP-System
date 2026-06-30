# Copyright (c) 2022, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework


def execute():
	for doctype in ["Purchase Order", "Purchase Receipt", "Purchase Invoice", "Supplier Quotation"]:
		terminal_framework.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_subcontracted = 0
				where is_subcontracted in ('', 'No') or is_subcontracted is null"""
		)
		terminal_framework.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_subcontracted = 1
				where is_subcontracted = 'Yes'"""
		)

		terminal_framework.reload_doc(terminal_framework.get_meta(doctype).module, "doctype", terminal_framework.scrub(doctype))
