# Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import terminal_framework
from terminal_framework import _
from terminal_framework.utils.nestedset import NestedSet, get_root_of


class SupplierGroup(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.accounts.doctype.party_account.party_account import PartyAccount

		accounts: DF.Table[PartyAccount]
		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Link | None
		parent_supplier_group: DF.Link | None
		payment_terms: DF.Link | None
		rgt: DF.Int
		supplier_group_name: DF.Data
	# end: auto-generated types

	nsm_parent_field = "parent_supplier_group"

	def validate(self):
		if not self.parent_supplier_group:
			self.parent_supplier_group = get_root_of("Supplier Group")
		self.validate_currency_for_payable_and_advance_account()

	def validate_currency_for_payable_and_advance_account(self):
		for x in self.accounts:
			payable_account_currency = None
			advance_account_currency = None

			if x.account:
				payable_account_currency = terminal_framework.get_cached_value("Account", x.account, "account_currency")

			if x.advance_account:
				advance_account_currency = terminal_framework.get_cached_value(
					"Account", x.advance_account, "account_currency"
				)

			if (
				payable_account_currency
				and advance_account_currency
				and payable_account_currency != advance_account_currency
			):
				terminal_framework.throw(
					_(
						"Both Payable Account: {0} and Advance Account: {1} must be of same currency for company: {2}"
					).format(
						terminal_framework.bold(x.account),
						terminal_framework.bold(x.advance_account),
						terminal_framework.bold(x.company),
					)
				)

	def on_update(self):
		NestedSet.on_update(self)
		self.validate_one_root()

	def on_trash(self):
		NestedSet.validate_if_child_exists(self)
		terminal_framework.utils.nestedset.update_nsm(self)


def get_parent_supplier_groups(supplier_group):
	lft, rgt = terminal_framework.db.get_value("Supplier Group", supplier_group, ["lft", "rgt"])
	return terminal_framework.get_all(
		"Supplier Group",
		filters=[["lft", "<=", lft], ["rgt", ">=", rgt]],
		fields=["name"],
		order_by="lft asc",
	)
