# Copyright (c) 2018, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	# Rename and reload the Land Unit and Linked Land Unit doctypes
	if terminal_framework.db.table_exists("Land Unit") and not terminal_framework.db.table_exists("Location"):
		terminal_framework.rename_doc("DocType", "Land Unit", "Location", force=True)

	terminal_framework.reload_doc("assets", "doctype", "location")

	if terminal_framework.db.table_exists("Linked Land Unit") and not terminal_framework.db.table_exists("Linked Location"):
		terminal_framework.rename_doc("DocType", "Linked Land Unit", "Linked Location", force=True)

	terminal_framework.reload_doc("assets", "doctype", "linked_location")

	if not terminal_framework.db.table_exists("Crop Cycle"):
		terminal_framework.reload_doc("agriculture", "doctype", "crop_cycle")

	# Rename the fields in related doctypes
	if "linked_land_unit" in terminal_framework.db.get_table_columns("Crop Cycle"):
		rename_field("Crop Cycle", "linked_land_unit", "linked_location")

	if "land_unit" in terminal_framework.db.get_table_columns("Linked Location"):
		rename_field("Linked Location", "land_unit", "location")

	if not terminal_framework.db.exists("Location", "All Land Units"):
		terminal_framework.get_doc({"doctype": "Location", "is_group": True, "location_name": "All Land Units"}).insert(
			ignore_permissions=True
		)

	if terminal_framework.db.table_exists("Land Unit"):
		land_units = terminal_framework.get_all("Land Unit", fields=["*"], order_by="lft")

		for land_unit in land_units:
			if not terminal_framework.db.exists("Location", land_unit.get("land_unit_name")):
				terminal_framework.get_doc(
					{
						"doctype": "Location",
						"location_name": land_unit.get("land_unit_name"),
						"parent_location": land_unit.get("parent_land_unit") or "All Land Units",
						"is_container": land_unit.get("is_container"),
						"is_group": land_unit.get("is_group"),
						"latitude": land_unit.get("latitude"),
						"longitude": land_unit.get("longitude"),
						"area": land_unit.get("area"),
						"location": land_unit.get("location"),
						"lft": land_unit.get("lft"),
						"rgt": land_unit.get("rgt"),
					}
				).insert(ignore_permissions=True)

	# Delete the Land Unit and Linked Land Unit doctypes
	if terminal_framework.db.table_exists("Land Unit"):
		terminal_framework.delete_doc("DocType", "Land Unit", force=1)

	if terminal_framework.db.table_exists("Linked Land Unit"):
		terminal_framework.delete_doc("DocType", "Linked Land Unit", force=1)
