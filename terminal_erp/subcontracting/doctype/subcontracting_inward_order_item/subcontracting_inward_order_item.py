# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework
from terminal_framework.model.document import Document
from terminal_framework.query_builder.functions import Sum


class SubcontractingInwardOrderItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		bom: DF.Link
		conversion_factor: DF.Float
		delivered_qty: DF.Float
		delivery_warehouse: DF.Link
		include_exploded_items: DF.Check
		item_code: DF.Link
		item_name: DF.Data
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		process_loss_qty: DF.Float
		produced_qty: DF.Float
		qty: DF.Float
		returned_qty: DF.Float
		sales_order_item: DF.Data | None
		stock_uom: DF.Link
		subcontracting_conversion_factor: DF.Float
	# end: auto-generated types

	pass

	def update_manufacturing_qty_fields(self):
		table = terminal_framework.qb.DocType("Work Order")
		query = (
			terminal_framework.qb.from_(table)
			.select(
				Sum(table.produced_qty).as_("produced_qty"),
				Sum(table.process_loss_qty).as_("process_loss_qty"),
			)
			.where((table.subcontracting_inward_order_item == self.name) & (table.docstatus == 1))
		)
		result = query.run(as_dict=True)[0]

		self.db_set("produced_qty", result.produced_qty)
		self.db_set("process_loss_qty", result.process_loss_qty)
