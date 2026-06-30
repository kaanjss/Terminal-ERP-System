# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import terminal_framework
from terminal_framework.model.document import Document


class DeliveryScheduleItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		conversion_factor: DF.Float
		delivery_date: DF.Date | None
		item_code: DF.Link | None
		qty: DF.Float
		sales_order: DF.Link | None
		sales_order_item: DF.Data | None
		stock_qty: DF.Float
		stock_uom: DF.Link | None
		uom: DF.Link | None
		warehouse: DF.Link | None
	# end: auto-generated types

	pass
