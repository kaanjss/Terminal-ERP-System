# Copyright (c) 2017, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from terminal_framework.model.document import Document


class IssueType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		description: DF.SmallText | None
	# end: auto-generated types

	pass
