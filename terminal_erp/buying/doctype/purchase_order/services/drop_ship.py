# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

"""Drop-ship item handling for Purchase Order."""

import terminal_framework
from terminal_framework import _


class DropShipService:
	def __init__(self, doc):
		self.doc = doc

	def update_dropship_received_qty(self, data: list[dict]) -> None:
		doc = self.doc
		if not data:
			terminal_framework.throw(_("Please select at least one item to update delivered quantity."))

		for d in data:
			item = next((item for item in doc.items if item.name == d.get("name")), None)

			if not item:
				terminal_framework.throw(
					_("Item with name {0} not found in the Purchase Order").format(terminal_framework.bold(d.get("name")))
				)

			if not item.delivered_by_supplier:
				terminal_framework.throw(
					_(
						"Item {0} is not a drop ship item. Only drop ship items can have Delivered Qty updated."
					).format(terminal_framework.bold(item.item_code))
				)

			if not item.has_permlevel_access_to("received_qty", permission_type="write"):
				terminal_framework.throw(
					_("You don't have permission to update Received Qty DocField for item {0}").format(
						terminal_framework.bold(item.item_code)
					)
				)

			if not d.get("qty_change"):
				terminal_framework.throw(
					_(
						"Item {0} has no changes in delivered quantity. Please unselect the row if you do not wish to update its quantity."
					).format(terminal_framework.bold(item.item_code))
				)

			if d.get("qty_change") < 0 and abs(d.get("qty_change")) > item.received_qty:
				terminal_framework.throw(
					_("Delivered Qty cannot be reduced by more than {0} for item {1}").format(
						item.received_qty, terminal_framework.bold(item.item_code)
					)
				)

			if d.get("qty_change") > 0 and item.received_qty + d.get("qty_change") > item.qty:
				terminal_framework.throw(
					_("Delivered Qty cannot be increased by more than {0} for item {1}").format(
						item.qty - item.received_qty, terminal_framework.bold(item.item_code)
					)
				)

			qty_change = item.received_qty + d.get("qty_change")
			item.db_set("received_qty", qty_change, update_modified=True)
			doc.add_comment(
				"Label",
				_("updated delivered quantity for item {0} to {1}").format(
					terminal_framework.bold(item.item_code), terminal_framework.bold(qty_change)
				),
			)
		doc.update_receiving_percentage()
		doc.set_status(update=True)
		self.update_delivered_qty_in_sales_order()

	def update_delivered_qty_in_sales_order(self) -> None:
		"""Update delivered qty in Sales Order for drop ship"""
		sales_orders_to_update = []
		for item in self.doc.items:
			if item.sales_order and item.delivered_by_supplier == 1:
				if item.sales_order not in sales_orders_to_update:
					sales_orders_to_update.append(item.sales_order)

		for so_name in sales_orders_to_update:
			so = terminal_framework.get_lazy_doc("Sales Order", so_name)
			so.update_delivery_status()
			so.set_status(update=True)
			so.notify_update()

	def set_received_qty_to_zero_for_drop_ship_items(self) -> None:
		for item in self.doc.items:
			if item.delivered_by_supplier:
				item.db_set("received_qty", 0)

	def has_drop_ship_item(self) -> bool:
		return any(d.delivered_by_supplier for d in self.doc.items)
