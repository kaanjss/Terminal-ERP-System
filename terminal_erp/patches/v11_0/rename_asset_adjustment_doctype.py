# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	if terminal_framework.db.table_exists("Asset Adjustment") and not terminal_framework.db.table_exists("Asset Value Adjustment"):
		terminal_framework.rename_doc("DocType", "Asset Adjustment", "Asset Value Adjustment", force=True)
		terminal_framework.reload_doc("assets", "doctype", "asset_value_adjustment")
