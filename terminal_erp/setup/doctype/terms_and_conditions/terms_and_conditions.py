# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import json

import terminal_framework
from terminal_framework import _, throw
from terminal_framework.model.document import Document
from terminal_framework.utils import cint
from terminal_framework.utils.jinja import validate_template


class TermsandConditions(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		buying: DF.Check
		copy_attachments_to_transaction: DF.Check
		disabled: DF.Check
		selling: DF.Check
		terms: DF.TextEditor | None
		title: DF.Data
	# end: auto-generated types

	def validate(self):
		if self.terms:
			validate_template(self.terms)
		if not cint(self.buying) and not cint(self.selling) and not cint(self.hr) and not cint(self.disabled):
			throw(_("At least one of the Applicable Modules should be selected"))


@terminal_framework.whitelist()
def get_terms_and_conditions(template_name: str, doc: str | dict):
	doc = terminal_framework.parse_json(doc)

	terms_and_conditions = terminal_framework.get_doc("Terms and Conditions", template_name)

	if terms_and_conditions.terms:
		return terminal_framework.render_template(terms_and_conditions.terms, doc)
