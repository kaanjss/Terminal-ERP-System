# Copyright (c) 2020, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import terminal_framework
from terminal_framework import _
from terminal_framework.model.document import Document


class JournalEntryTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.accounts.doctype.journal_entry_template_account.journal_entry_template_account import (
			JournalEntryTemplateAccount,
		)

		accounts: DF.Table[JournalEntryTemplateAccount]
		company: DF.Link
		is_opening: DF.Literal["No", "Yes"]
		multi_currency: DF.Check
		naming_series: DF.Literal
		template_title: DF.Data
		voucher_type: DF.Literal[
			"Journal Entry",
			"Inter Company Journal Entry",
			"Bank Entry",
			"Cash Entry",
			"Credit Card Entry",
			"Debit Note",
			"Credit Note",
			"Contra Entry",
			"Excise Entry",
			"Write Off Entry",
			"Opening Entry",
			"Depreciation Entry",
			"Exchange Rate Revaluation",
		]
	# end: auto-generated types

	def validate(self):
		self.validate_party()

	def validate_party(self):
		"""
		Loop over all accounts and see if party and party type is set correctly
		"""
		for account in self.accounts:
			if account.party_type:
				account_type = terminal_framework.get_cached_value("Account", account.account, "account_type")
				if account_type not in ["Receivable", "Payable"]:
					terminal_framework.throw(
						_(
							"Check row {0} for account {1}: Party Type is only allowed for Receivable or Payable accounts"
						).format(account.idx, account.account)
					)

			if account.party and not account.party_type:
				terminal_framework.throw(
					_("Check row {0} for account {1}: Party is only allowed if Party Type is set").format(
						account.idx, account.account
					)
				)


@terminal_framework.whitelist()
def get_naming_series():
	return terminal_framework.get_meta("Journal Entry").get_field("naming_series").options
