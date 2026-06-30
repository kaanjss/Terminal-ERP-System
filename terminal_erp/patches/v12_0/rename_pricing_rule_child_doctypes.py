# Copyright (c) 2017, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework

doctypes = {
	"Price Discount Slab": "Promotional Scheme Price Discount",
	"Product Discount Slab": "Promotional Scheme Product Discount",
	"Apply Rule On Item Code": "Pricing Rule Item Code",
	"Apply Rule On Item Group": "Pricing Rule Item Group",
	"Apply Rule On Brand": "Pricing Rule Brand",
}


def execute():
	for old_doc, new_doc in doctypes.items():
		if not terminal_framework.db.table_exists(new_doc) and terminal_framework.db.table_exists(old_doc):
			terminal_framework.rename_doc("DocType", old_doc, new_doc)
			terminal_framework.reload_doc("accounts", "doctype", terminal_framework.scrub(new_doc))
			terminal_framework.delete_doc("DocType", old_doc)
