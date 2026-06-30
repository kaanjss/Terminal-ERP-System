# Copyright (c) 2017, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from collections import Counter

import terminal_framework
from terminal_framework import _
from terminal_framework.model.document import Document


class POSSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.accounts.doctype.pos_field.pos_field import POSField
		from terminal_erp.accounts.doctype.pos_search_fields.pos_search_fields import POSSearchFields

		invoice_fields: DF.Table[POSField]
		invoice_type: DF.Literal["Sales Invoice", "POS Invoice"]
		pos_search_fields: DF.Table[POSSearchFields]
		post_change_gl_entries: DF.Check
	# end: auto-generated types

	def validate(self):
		old_doc = self.get_doc_before_save()

		if old_doc.invoice_type != self.invoice_type:
			self.validate_invoice_type()

		self.validate_invoice_fields()

	def validate_invoice_fields(self):
		invoice_fields = [field.fieldname for field in self.invoice_fields]
		duplicate_invoice_fields = {key for key, value in Counter(invoice_fields).items() if value > 1}

		if len(duplicate_invoice_fields):
			for field in duplicate_invoice_fields:
				terminal_framework.throw(
					title=_("Duplicate POS Fields"), msg=_("'{0}' has been already added.").format(field)
				)

	def validate_invoice_type(self):
		pos_opening_entries_count = terminal_framework.db.count(
			"POS Opening Entry", filters={"docstatus": 1, "status": "Open"}
		)
		if pos_opening_entries_count:
			terminal_framework.throw(
				_("{0} cannot be changed with opened Opening Entries.").format(
					terminal_framework.bold(_("Invoice Type"))
				),
				title=_("Invoice Document Type Selection Error"),
			)
