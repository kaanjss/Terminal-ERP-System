# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import terminal_framework
from terminal_framework.model.document import Document


class PaymentGatewayAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		company: DF.Link
		currency: DF.ReadOnly | None
		is_default: DF.Check
		message: DF.SmallText | None
		payment_account: DF.Link
		payment_channel: DF.Literal["", "Email", "Phone"]
		payment_gateway: DF.Link
	# end: auto-generated types

	def autoname(self):
		abbr = terminal_framework.db.get_value("Company", self.company, "abbr")
		self.name = self.payment_gateway + " - " + self.currency + " - " + abbr

	def validate(self):
		self.currency = terminal_framework.get_cached_value("Account", self.payment_account, "account_currency")

		self.update_default_payment_gateway()
		self.set_as_default_if_not_set()

	def update_default_payment_gateway(self):
		if self.is_default:
			terminal_framework.db.set_value(
				"Payment Gateway Account",
				{"is_default": 1, "name": ["!=", self.name], "company": self.company},
				"is_default",
				0,
			)

	def set_as_default_if_not_set(self):
		if not terminal_framework.db.exists(
			"Payment Gateway Account", {"is_default": 1, "name": ("!=", self.name), "company": self.company}
		):
			self.is_default = 1
