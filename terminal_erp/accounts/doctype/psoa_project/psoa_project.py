# Copyright (c) 2020, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import terminal_framework
from terminal_framework.model.document import Document


class PSOAProject(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		project_name: DF.Link | None
	# end: auto-generated types

	pass
