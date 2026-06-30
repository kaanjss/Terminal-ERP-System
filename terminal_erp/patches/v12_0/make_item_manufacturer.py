# Copyright (c) 2017, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("stock", "doctype", "item_manufacturer")

	item_manufacturer = []
	for d in terminal_framework.db.sql(
		""" SELECT name, manufacturer, manufacturer_part_no, creation, owner
		FROM `tabItem` WHERE manufacturer is not null and manufacturer != ''""",
		as_dict=1,
	):
		item_manufacturer.append(
			(
				terminal_framework.generate_hash("", 10),
				d.name,
				d.manufacturer,
				d.manufacturer_part_no,
				d.creation,
				d.owner,
			)
		)

	if item_manufacturer:
		terminal_framework.db.sql(
			"""
			INSERT INTO `tabItem Manufacturer`
			(`name`, `item_code`, `manufacturer`, `manufacturer_part_no`, `creation`, `owner`)
			VALUES {}""".format(", ".join(["%s"] * len(item_manufacturer))),
			tuple(item_manufacturer),
		)
