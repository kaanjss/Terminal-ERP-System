# Copyright (c) 2017, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("assets", "doctype", "asset_finance_book")
	terminal_framework.reload_doc("assets", "doctype", "depreciation_schedule")
	terminal_framework.reload_doc("assets", "doctype", "asset_category")
	terminal_framework.reload_doc("assets", "doctype", "asset")
	terminal_framework.reload_doc("assets", "doctype", "asset_movement")
	terminal_framework.reload_doc("assets", "doctype", "asset_category_account")

	if terminal_framework.db.has_column("Asset", "warehouse"):
		terminal_framework.db.sql(
			""" update `tabAsset` ast, `tabWarehouse` wh
			set ast.location = wh.warehouse_name where ast.warehouse = wh.name"""
		)

		for d in terminal_framework.get_all("Asset"):
			doc = terminal_framework.get_doc("Asset", d.name)
			if doc.calculate_depreciation:
				fb = doc.append(
					"finance_books",
					{
						"depreciation_method": doc.depreciation_method,
						"total_number_of_depreciations": doc.total_number_of_depreciations,
						"frequency_of_depreciation": doc.frequency_of_depreciation,
						"depreciation_start_date": doc.next_depreciation_date,
						"expected_value_after_useful_life": doc.expected_value_after_useful_life,
						"value_after_depreciation": doc.value_after_depreciation,
					},
				)

				fb.db_update()

		terminal_framework.db.sql(
			""" update `tabDepreciation Schedule` ds, `tabAsset` ast
			set ds.depreciation_method = ast.depreciation_method, ds.finance_book_id = 1 where ds.parent = ast.name """
		)

		for category in terminal_framework.get_all("Asset Category"):
			asset_category_doc = terminal_framework.get_doc("Asset Category", category)
			row = asset_category_doc.append(
				"finance_books",
				{
					"depreciation_method": asset_category_doc.depreciation_method,
					"total_number_of_depreciations": asset_category_doc.total_number_of_depreciations,
					"frequency_of_depreciation": asset_category_doc.frequency_of_depreciation,
				},
			)

			row.db_update()
