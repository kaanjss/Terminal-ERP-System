# Copyright (c) 2020, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import terminal_framework
from terminal_framework.model.document import Document


class SubOperation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		description: DF.SmallText | None
		operation: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		time_in_mins: DF.Float
	# end: auto-generated types

	pass
