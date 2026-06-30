# Copyright (c) 2026, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import terminal_framework
from terminal_framework.model.document import Document


class BankStatementImportLogColumnMap(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		header_text: DF.Data
		index: DF.Int
		maps_to: DF.Literal[
			"Do not import",
			"Date",
			"Withdrawal",
			"Deposit",
			"Amount",
			"Description",
			"Reference",
			"Transaction Type",
			"Debit/Credit",
			"Balance",
			"Included Fee",
			"Excluded Fee",
			"Party Name/Account Holder",
			"Party Account No.",
			"Party IBAN",
		]
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		variable: DF.Data | None
	# end: auto-generated types

	pass
