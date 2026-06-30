# Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from terminal_framework.model.document import Document


class BankTransactionPayments(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		allocated_amount: DF.Currency
		clearance_date: DF.Date | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		payment_document: DF.Link
		payment_entry: DF.DynamicLink
		reconciliation_type: DF.Literal["Matched", "Voucher Created"]
	# end: auto-generated types

	pass
