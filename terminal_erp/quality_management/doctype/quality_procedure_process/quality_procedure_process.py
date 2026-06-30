# Copyright (c) 2019, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import terminal_framework
from terminal_framework.model.document import Document


class QualityProcedureProcess(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		procedure: DF.Link | None
		process_description: DF.TextEditor | None
	# end: auto-generated types

	pass
