# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import datetime

import terminal_framework
from terminal_framework import _
from terminal_framework.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,
)
from terminal_framework.model.document import Document
from terminal_framework.utils import comma_and, get_link_to_form


class BankAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		account: DF.Link | None
		account_name: DF.Data
		account_subtype: DF.Link | None
		account_type: DF.Link | None
		bank: DF.Link
		bank_account_no: DF.Data | None
		branch_code: DF.Data | None
		company: DF.Link | None
		disabled: DF.Check
		iban: DF.Data | None
		integration_id: DF.Data | None
		is_company_account: DF.Check
		is_credit_card: DF.Check
		is_default: DF.Check
		last_integration_date: DF.Date | None
		mask: DF.Data | None
		party: DF.DynamicLink | None
		party_type: DF.Link | None
		statement_password: DF.Password | None
	# end: auto-generated types

	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def autoname(self):
		self.name = self.account_name + " - " + self.bank

	def on_trash(self):
		delete_contact_and_address("Bank Account", self.name)

		# Delete all bank balances
		terminal_framework.db.delete("Bank Account Balance", filters={"bank_account": self.name})

	def validate(self):
		self.validate_is_company_account()
		self.update_default_bank_account()

	def validate_is_company_account(self):
		if self.is_company_account:
			if not self.company:
				terminal_framework.throw(_("Company is mandatory for company account"))

			if not self.account:
				terminal_framework.throw(_("Company Account is mandatory"))

			self.validate_account()

	def validate_account(self):
		if accounts := terminal_framework.db.get_all(
			"Bank Account", filters={"account": self.account, "name": ["!=", self.name]}, as_list=1
		):
			terminal_framework.throw(
				_("'{0}' account is already used by {1}. Use another account.").format(
					terminal_framework.bold(self.account),
					terminal_framework.bold(comma_and([get_link_to_form(self.doctype, x[0]) for x in accounts])),
				)
			)

	def update_default_bank_account(self):
		if self.is_default and not self.disabled:
			terminal_framework.db.set_value(
				"Bank Account",
				{
					"party_type": self.party_type,
					"party": self.party,
					"is_company_account": self.is_company_account,
					"company": self.company,
					"is_default": 1,
					"disabled": 0,
				},
				"is_default",
				0,
			)


def get_party_bank_account(party_type, party):
	return terminal_framework.db.get_value(
		"Bank Account",
		{"party_type": party_type, "party": party, "is_default": 1, "disabled": 0},
		"name",
	)


def get_default_company_bank_account(company, party_type, party):
	default_company_bank_account = terminal_framework.db.get_value(party_type, party, "default_bank_account")
	if default_company_bank_account:
		if company != terminal_framework.get_cached_value("Bank Account", default_company_bank_account, "company"):
			default_company_bank_account = None

	if not default_company_bank_account:
		default_company_bank_account = terminal_framework.db.get_value(
			"Bank Account", {"company": company, "is_company_account": 1, "is_default": 1}
		)

	return default_company_bank_account


@terminal_framework.whitelist()
def get_bank_account_details(bank_account: str):
	terminal_framework.has_permission("Bank Account", doc=bank_account, ptype="read", throw=True)
	return terminal_framework.get_cached_value(
		"Bank Account", bank_account, ["account", "bank", "bank_account_no"], as_dict=1
	)


@terminal_framework.whitelist(methods=["GET"])
def get_list(company: str, show_disabled: bool = False):
	"""
	Returns a list of bank accounts for a company - with the account currency

	@param company: The company to get the bank accounts for
	@param show_disabled: Whether to show disabled bank accounts
	@return: A list of bank accounts
	"""

	filters = {"is_company_account": 1, "company": company}
	if not show_disabled:
		filters["disabled"] = 0

	bank_accounts = terminal_framework.get_list(
		"Bank Account",
		filters=filters,
		order_by="is_default desc",
		fields=[
			"name",
			"account",
			"company",
			"account_name",
			"is_default",
			"bank",
			"account_type",
			"account_subtype",
			"bank_account_no",
			"last_integration_date",
			"is_credit_card",
		],
	)

	for bank_account in bank_accounts:
		bank_account.account_currency = terminal_framework.get_cached_value(
			"Account", bank_account.account, "account_currency"
		)

	return bank_accounts


@terminal_framework.whitelist(methods=["GET"])
def get_closing_balance_as_per_statement(bank_account: str, date: str):
	"""
	Get the closing balance as per statement for a bank account and date
	"""
	latest_balance = terminal_framework.get_list(
		"Bank Account Balance",
		filters={"bank_account": bank_account, "date": ["<=", date]},
		fields=["balance", "date"],
		order_by="date desc",
		limit=1,
	)

	if latest_balance:
		return {"balance": latest_balance[0].balance, "date": latest_balance[0].date}
	return {"balance": 0, "date": None}


@terminal_framework.whitelist()
def set_closing_balance_as_per_statement(bank_account: str, date: str | datetime.date, balance: float):
	"""
	Set the closing balance as per statement for a bank account and date
	"""

	existing = terminal_framework.db.exists("Bank Account Balance", {"bank_account": bank_account, "date": date})

	if existing:
		doc = terminal_framework.get_doc("Bank Account Balance", existing)
		doc.balance = balance
		doc.save()
	else:
		doc = terminal_framework.new_doc("Bank Account Balance")
		doc.bank_account = bank_account
		doc.date = date
		doc.balance = balance
		doc.save()
