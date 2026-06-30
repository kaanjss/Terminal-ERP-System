# Copyright (c) 2017, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import terminal_framework
from terminal_framework import _
from terminal_framework.model.document import Document


class ProjectType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		description: DF.Text | None
		project_type: DF.Data
	# end: auto-generated types

	def on_trash(self):
		if self.name == "External":
			terminal_framework.throw(_("You cannot delete Project Type 'External'"))
