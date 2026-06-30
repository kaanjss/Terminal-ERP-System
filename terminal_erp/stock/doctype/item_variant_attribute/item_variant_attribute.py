# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt


from terminal_framework.model.document import Document


class ItemVariantAttribute(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		attribute: DF.Link
		attribute_value: DF.Data | None
		disabled: DF.Check
		from_range: DF.Float
		increment: DF.Float
		numeric_values: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		to_range: DF.Float
		variant_of: DF.Link | None
	# end: auto-generated types

	pass
