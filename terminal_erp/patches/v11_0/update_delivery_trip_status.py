# Copyright (c) 2017, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("setup", "doctype", "global_defaults", force=True)
	terminal_framework.reload_doc("stock", "doctype", "delivery_trip")
	terminal_framework.reload_doc("stock", "doctype", "delivery_stop", force=True)

	for trip in terminal_framework.get_all("Delivery Trip"):
		trip_doc = terminal_framework.get_doc("Delivery Trip", trip.name)

		status = {0: "Draft", 1: "Scheduled", 2: "Cancelled"}[trip_doc.docstatus]

		if trip_doc.docstatus == 1:
			visited_stops = [stop.visited for stop in trip_doc.delivery_stops]
			if all(visited_stops):
				status = "Completed"
			elif any(visited_stops):
				status = "In Transit"

		terminal_framework.db.set_value("Delivery Trip", trip.name, "status", status, update_modified=False)
