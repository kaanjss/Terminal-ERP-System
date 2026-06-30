# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import terminal_framework
from terminal_framework.model.document import Document


class PeggedCurrencies(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.accounts.doctype.pegged_currencies.pegged_currencies import PeggedCurrencies

		pegged_currency_item: DF.Table[PeggedCurrencies]
	# end: auto-generated types

	pass
