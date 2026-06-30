# Copyright (c) 2017, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from terminal_framework.model.document import Document


class SupplierScorecardScoringVariable(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		description: DF.SmallText | None
		param_name: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		path: DF.Data | None
		value: DF.Float
		variable_label: DF.Link
	# end: auto-generated types

	pass
