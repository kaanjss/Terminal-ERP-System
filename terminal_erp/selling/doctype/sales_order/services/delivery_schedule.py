# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

"""Delivery schedule management for Sales Order Items."""

import terminal_framework
from terminal_framework.utils import parse_json


class DeliveryScheduleService:
	def __init__(self, doc):
		self.doc = doc

	def get_delivery_schedule(self, sales_order_item: str) -> list[dict]:
		return terminal_framework.get_all(
			"Delivery Schedule Item",
			filters={"sales_order_item": sales_order_item, "sales_order": self.doc.name},
			fields=["delivery_date", "qty", "name"],
			order_by="delivery_date asc",
		)

	def create_delivery_schedule(self, child_row: dict | terminal_framework._dict, schedules: str | list[dict]) -> None:
		if isinstance(child_row, dict):
			child_row = terminal_framework._dict(child_row)

		if isinstance(schedules, str):
			schedules = parse_json(schedules)

		names = []
		first_delivery_date = None
		for row in schedules:
			row = terminal_framework._dict(row)

			if not first_delivery_date:
				first_delivery_date = row.delivery_date

			data = {
				"delivery_date": row.delivery_date,
				"qty": row.qty,
				"uom": child_row.uom,
				"stock_uom": child_row.stock_uom,
				"item_code": child_row.item_code,
				"conversion_factor": child_row.conversion_factor or 1.0,
				"warehouse": child_row.warehouse,
				"sales_order_item": child_row.name,
				"sales_order": self.doc.name,
				"stock_qty": row.qty * (child_row.conversion_factor or 1.0),
			}

			if terminal_framework.db.exists("Delivery Schedule Item", row.name):
				doc = terminal_framework.get_doc("Delivery Schedule Item", row.name)
			else:
				doc = terminal_framework.new_doc("Delivery Schedule Item")

			doc.update(data)
			doc.save(ignore_permissions=True)
			names.append(doc.name)

		if names:
			self.delete_delivery_schedule_items(child_row.name, names)

		if first_delivery_date:
			self.update_delivery_date_based_on_schedule(child_row, first_delivery_date)

	def update_delivery_date_based_on_schedule(self, child_row, first_delivery_date) -> None:
		for row in self.doc.items:
			if row.name == child_row.name:
				if first_delivery_date:
					row.delivery_date = first_delivery_date
				break

		self.doc.save()

	def delete_delivery_schedule_items(
		self, sales_order_item: str | None = None, ignore_names: list | None = None
	) -> None:
		"""Delete delivery schedule items."""
		doctype = terminal_framework.qb.DocType("Delivery Schedule Item")

		query = terminal_framework.qb.from_(doctype).delete().where(doctype.sales_order == self.doc.name)

		if ignore_names:
			query = query.where(doctype.name.notin(ignore_names))

		if sales_order_item:
			query = query.where(doctype.sales_order_item == sales_order_item)

		query.run()

	def delete_removed_delivery_schedule_items(self) -> None:
		items = [d.name for d in self.doc.get("items")]
		doctype = terminal_framework.qb.DocType("Delivery Schedule Item")
		terminal_framework.qb.from_(doctype).delete().where(
			(doctype.sales_order == self.doc.name) & (doctype.sales_order_item.notin(items))
		).run()
