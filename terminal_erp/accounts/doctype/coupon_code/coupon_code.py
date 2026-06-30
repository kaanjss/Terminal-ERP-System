# Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import terminal_framework
from terminal_framework import _
from terminal_framework.model.document import Document
from terminal_framework.utils import strip


class CouponCode(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		amended_from: DF.Link | None
		coupon_code: DF.Data | None
		coupon_name: DF.Data
		coupon_type: DF.Literal["Promotional", "Gift Card"]
		customer: DF.Link | None
		description: DF.TextEditor | None
		from_external_ecomm_platform: DF.Check
		maximum_use: DF.Int
		pricing_rule: DF.Link | None
		used: DF.Int
		valid_from: DF.Date | None
		valid_upto: DF.Date | None
	# end: auto-generated types

	def autoname(self):
		self.coupon_name = strip(self.coupon_name)
		self.name = self.coupon_name

		if not self.coupon_code:
			if self.coupon_type == "Promotional":
				self.coupon_code = "".join(i for i in self.coupon_name if not i.isdigit())[0:8].upper()
			elif self.coupon_type == "Gift Card":
				self.coupon_code = terminal_framework.generate_hash()[:10].upper()

	def validate(self):
		if self.coupon_type == "Gift Card":
			self.maximum_use = 1
			if not self.customer:
				terminal_framework.throw(_("Please select the customer."))
