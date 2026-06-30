# Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from terminal_framework.model.document import Document


class ItemTaxTemplateDetail(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		not_applicable: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		tax_rate: DF.Float
		tax_type: DF.Link
	# end: auto-generated types

	pass
