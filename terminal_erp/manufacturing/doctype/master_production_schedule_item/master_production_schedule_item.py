# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import terminal_framework
from terminal_framework.model.document import Document


class MasterProductionScheduleItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		bom_no: DF.Link | None
		cumulative_lead_time: DF.Int
		delivery_date: DF.Date | None
		item_code: DF.Link | None
		item_name: DF.Data | None
		order_release_date: DF.Date | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		planned_qty: DF.Float
		uom: DF.Link | None
		warehouse: DF.Link | None
	# end: auto-generated types

	pass
