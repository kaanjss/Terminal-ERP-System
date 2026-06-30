# Copyright (c) 2021, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework
from terminal_framework import _
from terminal_framework.model.document import Document

from terminal_erp import get_region


class SouthAfricaVATSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.accounts.doctype.south_africa_vat_account.south_africa_vat_account import (
			SouthAfricaVATAccount,
		)

		company: DF.Link
		vat_accounts: DF.Table[SouthAfricaVATAccount]
	# end: auto-generated types

	def validate(self):
		self.validate_company_region()

	def validate_company_region(self):
		if self.company and get_region(self.company) != "South Africa":
			terminal_framework.throw(_("Company {0} is not in South Africa.").format(terminal_framework.bold(self.company)))
