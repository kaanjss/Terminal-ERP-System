# Copyright (c) 2026, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import terminal_framework
from terminal_framework.model.document import Document


class BOMSecondaryItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		base_cost: DF.Currency
		conversion_factor: DF.Float
		cost: DF.Currency
		cost_allocation_per: DF.Percent
		description: DF.TextEditor | None
		image: DF.AttachImage | None
		is_legacy: DF.Check
		item_code: DF.Link
		item_name: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		process_loss_per: DF.Percent
		process_loss_qty: DF.Float
		qty: DF.Float
		rate: DF.Currency
		secondary_item_type: DF.Literal["", "Co-Product", "By-Product", "Scrap", "Additional Finished Good"]
		stock_qty: DF.Float
		stock_uom: DF.Link | None
		uom: DF.Link
	# end: auto-generated types

	pass
