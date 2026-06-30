# Copyright (c) 2019, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import terminal_framework
from terminal_framework.model.document import Document


class QualityActionResolution(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		completion_by: DF.Date | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		problem: DF.LongText | None
		resolution: DF.TextEditor | None
		responsible: DF.Link | None
		status: DF.Literal["Open", "Completed"]
	# end: auto-generated types

	pass
