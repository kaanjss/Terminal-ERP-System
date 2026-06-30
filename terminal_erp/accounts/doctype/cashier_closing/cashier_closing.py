# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework
from terminal_framework import _
from terminal_framework.model.document import Document
from terminal_framework.query_builder.functions import Sum
from terminal_framework.utils import flt


class CashierClosing(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.accounts.doctype.cashier_closing_payments.cashier_closing_payments import (
			CashierClosingPayments,
		)

		amended_from: DF.Link | None
		custody: DF.Float
		date: DF.Date | None
		expense: DF.Float
		from_time: DF.Time
		naming_series: DF.Literal["POS-CLO-"]
		net_amount: DF.Float
		outstanding_amount: DF.Float
		payments: DF.Table[CashierClosingPayments]
		returns: DF.Float
		time: DF.Time
		user: DF.Link
	# end: auto-generated types

	def validate(self):
		self.validate_time()

	def before_save(self):
		self.get_outstanding()
		self.make_calculations()

	def get_outstanding(self):
		si = terminal_framework.qb.DocType("Sales Invoice")
		values = (
			terminal_framework.qb.from_(si)
			.select(Sum(si.outstanding_amount))
			.where(
				(si.posting_date == self.date)
				& (si.posting_time >= self.from_time)
				& (si.posting_time <= self.time)
				& (si.owner == self.user)
			)
			.run()
		)
		self.outstanding_amount = flt(values[0][0] if values else 0)

	def make_calculations(self):
		total = 0.00
		for i in self.payments:
			total += flt(i.amount)

		self.net_amount = (
			total + self.outstanding_amount + flt(self.expense) - flt(self.custody) + flt(self.returns)
		)

	def validate_time(self):
		if self.from_time >= self.time:
			terminal_framework.throw(_("From Time Should Be Less Than To Time"))
