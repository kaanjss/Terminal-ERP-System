# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# For license information, please see license.txt


from terminal_framework.model.document import Document


class LandedCostTaxesandCharges(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		account_currency: DF.Link | None
		amount: DF.Currency
		base_amount: DF.Currency
		description: DF.SmallText
		exchange_rate: DF.Float
		expense_account: DF.Link | None
		has_corrective_cost: DF.Check
		has_operating_cost: DF.Check
		operating_component: DF.Data | None
		operation_id: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		qty: DF.Float
	# end: auto-generated types

	pass
