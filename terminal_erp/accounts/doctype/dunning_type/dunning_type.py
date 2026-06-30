# Copyright (c) 2020, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import terminal_framework
from terminal_framework.model.document import Document


class DunningType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.accounts.doctype.dunning_letter_text.dunning_letter_text import DunningLetterText

		company: DF.Link
		cost_center: DF.Link | None
		dunning_fee: DF.Currency
		dunning_letter_text: DF.Table[DunningLetterText]
		dunning_type: DF.Data
		income_account: DF.Link | None
		is_default: DF.Check
		rate_of_interest: DF.Float
	# end: auto-generated types

	def autoname(self):
		company_abbr = terminal_framework.get_value("Company", self.company, "abbr")
		self.name = f"{self.dunning_type} - {company_abbr}"
