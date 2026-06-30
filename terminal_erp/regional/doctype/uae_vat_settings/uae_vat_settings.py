# Copyright (c) 2020, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import terminal_framework
from terminal_framework.model.document import Document


class UAEVATSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.regional.doctype.uae_vat_account.uae_vat_account import UAEVATAccount

		company: DF.Link
		uae_vat_accounts: DF.Table[UAEVATAccount]
	# end: auto-generated types

	pass
