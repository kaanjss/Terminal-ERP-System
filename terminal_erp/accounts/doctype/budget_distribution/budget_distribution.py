# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import terminal_framework
from terminal_framework.model.document import Document


class BudgetDistribution(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		amount: DF.Currency
		end_date: DF.Date
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		percent: DF.Percent
		start_date: DF.Date
	# end: auto-generated types

	pass
