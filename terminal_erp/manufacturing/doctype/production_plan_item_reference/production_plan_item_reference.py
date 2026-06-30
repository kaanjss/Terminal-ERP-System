# Copyright (c) 2021, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import terminal_framework
from terminal_framework.model.document import Document


class ProductionPlanItemReference(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		item_reference: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		qty: DF.Float
		sales_order: DF.Link | None
		sales_order_item: DF.Data | None
	# end: auto-generated types

	pass
