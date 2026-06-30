# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import terminal_framework
from terminal_framework.model.document import Document


class SalesInvoiceReference(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		customer: DF.Link
		grand_total: DF.Currency
		is_return: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		posting_date: DF.Date
		return_against: DF.Link | None
		sales_invoice: DF.Link
	# end: auto-generated types

	pass
