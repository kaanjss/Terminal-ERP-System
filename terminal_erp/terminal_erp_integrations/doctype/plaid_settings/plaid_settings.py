# Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import json

import terminal_framework
from terminal_framework import _
from terminal_framework.desk.doctype.tag.tag import add_tag
from terminal_framework.model.document import Document
from terminal_framework.utils import add_months, formatdate, getdate, sbool, today
from plaid.errors import ItemError

from terminal_erp.terminal_erp_integrations.doctype.plaid_settings.plaid_connector import PlaidConnector


class PlaidSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		automatic_sync: DF.Check
		enable_european_access: DF.Check
		enabled: DF.Check
		plaid_client_id: DF.Data | None
		plaid_env: DF.Literal["sandbox", "development", "production"]
		plaid_secret: DF.Password | None
	# end: auto-generated types

	@staticmethod
	@terminal_framework.whitelist()
	def get_link_token():
		plaid = PlaidConnector()
		return plaid.get_link_token()


@terminal_framework.whitelist()
def get_plaid_configuration():
	if terminal_framework.db.get_single_value("Plaid Settings", "enabled"):
		plaid_settings = terminal_framework.get_single("Plaid Settings")
		return {
			"plaid_env": plaid_settings.plaid_env,
			"link_token": plaid_settings.get_link_token(),
			"client_name": terminal_framework.local.site,
		}

	return "disabled"


@terminal_framework.whitelist()
def add_institution(token: str, response: str | dict):
	response = terminal_framework.parse_json(response)

	plaid = PlaidConnector()
	access_token = plaid.get_access_token(token)
	bank = None

	if not terminal_framework.db.exists("Bank", response["institution"]["name"]):
		try:
			bank = terminal_framework.get_doc(
				{
					"doctype": "Bank",
					"bank_name": response["institution"]["name"],
					"plaid_access_token": access_token,
				}
			)
			bank.insert()
		except Exception:
			terminal_framework.db.rollback()
			terminal_framework.log_error("Plaid Link Error")
	else:
		bank = terminal_framework.get_doc("Bank", response["institution"]["name"])
		bank.plaid_access_token = access_token
		bank.save()

	return bank


@terminal_framework.whitelist()
def add_bank_accounts(response: str | dict, bank: str | dict, company: str):
	response = terminal_framework.parse_json(response)
	bank = terminal_framework.parse_json(bank)
	result = []

	parent_gl_account = terminal_framework.db.get_all(
		"Account", {"company": company, "account_type": "Bank", "is_group": 1, "disabled": 0}
	)
	if not parent_gl_account:
		terminal_framework.throw(
			_(
				"Please setup and enable a group account with the Account Type - {0} for the company {1}"
			).format(terminal_framework.bold(_("Bank")), company)
		)

	for account in response["accounts"]:
		acc_type = terminal_framework.db.get_value("Bank Account Type", account["type"])
		if not acc_type:
			add_account_type(account["type"])

		acc_subtype = terminal_framework.db.get_value("Bank Account Subtype", account["subtype"])
		if not acc_subtype:
			add_account_subtype(account["subtype"])

		bank_account_name = "{} - {}".format(account["name"], bank["bank_name"])
		existing_bank_account = terminal_framework.db.exists("Bank Account", bank_account_name)

		if not existing_bank_account:
			try:
				# savepoint so a failed insert doesn't poison the transaction on postgres
				terminal_framework.db.savepoint("plaid_bank_account")
				gl_account = terminal_framework.get_doc(
					{
						"doctype": "Account",
						"account_name": account["name"] + " - " + response["institution"]["name"],
						"parent_account": parent_gl_account[0].name,
						"account_type": "Bank",
						"company": company,
					}
				)
				gl_account.insert(ignore_if_duplicate=True)

				new_account = terminal_framework.get_doc(
					{
						"doctype": "Bank Account",
						"bank": bank["bank_name"],
						"account": gl_account.name,
						"account_name": account["name"],
						"account_type": account.get("type", ""),
						"account_subtype": account.get("subtype", ""),
						"mask": account.get("mask", ""),
						"integration_id": account["id"],
						"is_company_account": 1,
						"company": company,
					}
				)
				new_account.insert()

				result.append(new_account.name)
			except terminal_framework.UniqueValidationError:
				terminal_framework.db.rollback(save_point="plaid_bank_account")  # preserve transaction in postgres
				terminal_framework.msgprint(
					_("Bank account {0} already exists and could not be created again").format(
						account["name"]
					)
				)
			except Exception:
				terminal_framework.db.rollback(save_point="plaid_bank_account")  # preserve transaction in postgres
				terminal_framework.log_error("Plaid Link Error")
				terminal_framework.throw(
					_("There was an error creating Bank Account while linking with Plaid."),
					title=_("Plaid Link Failed"),
				)

		else:
			terminal_framework.db.savepoint("plaid_update_account")
			try:
				existing_account = terminal_framework.get_doc("Bank Account", existing_bank_account)
				existing_account.update(
					{
						"bank": bank["bank_name"],
						"account_name": account["name"],
						"account_type": account.get("type", ""),
						"account_subtype": account.get("subtype", ""),
						"mask": account.get("mask", ""),
						"integration_id": account["id"],
					}
				)
				existing_account.save()
				result.append(existing_bank_account)
			except Exception:
				terminal_framework.db.rollback(save_point="plaid_update_account")
				terminal_framework.log_error("Plaid Link Error")
				terminal_framework.throw(
					_("There was an error updating Bank Account {0} while linking with Plaid.").format(
						existing_bank_account
					),
					title=_("Plaid Link Failed"),
				)

	return result


def add_account_type(account_type):
	try:
		terminal_framework.get_doc({"doctype": "Bank Account Type", "account_type": account_type}).insert()
	except Exception:
		terminal_framework.throw(terminal_framework.get_traceback())


def add_account_subtype(account_subtype):
	try:
		terminal_framework.get_doc({"doctype": "Bank Account Subtype", "account_subtype": account_subtype}).insert()
	except Exception:
		terminal_framework.throw(terminal_framework.get_traceback())


def sync_transactions(bank, bank_account):
	"""Sync transactions based on the last integration date as the start date, after sync is completed
	add the transaction date of the oldest transaction as the last integration date."""
	last_transaction_date = terminal_framework.db.get_value("Bank Account", bank_account, "last_integration_date")
	if last_transaction_date:
		start_date = formatdate(last_transaction_date, "YYYY-MM-dd")
	else:
		start_date = formatdate(add_months(today(), -12), "YYYY-MM-dd")
	end_date = formatdate(today(), "YYYY-MM-dd")

	try:
		transactions = get_transactions(
			bank=bank, bank_account=bank_account, start_date=start_date, end_date=end_date
		)

		result = []
		if transactions:
			for transaction in reversed(transactions):
				result += new_bank_transaction(transaction)

		if result:
			last_transaction_date = terminal_framework.db.get_value("Bank Transaction", result.pop(), "date")

			terminal_framework.logger().info(
				f"Plaid added {len(result)} new Bank Transactions from '{bank_account}' between {start_date} and {end_date}"
			)

			terminal_framework.db.set_value("Bank Account", bank_account, "last_integration_date", last_transaction_date)
	except Exception:
		terminal_framework.log_error(terminal_framework.get_traceback(), _("Plaid transactions sync error"))


def get_transactions(bank, bank_account=None, start_date=None, end_date=None):
	access_token = None

	if bank_account:
		related_bank = terminal_framework.db.get_values(
			"Bank Account", bank_account, ["bank", "integration_id"], as_dict=True
		)
		access_token = terminal_framework.db.get_value("Bank", related_bank[0].bank, "plaid_access_token")
		account_id = related_bank[0].integration_id
	else:
		access_token = terminal_framework.db.get_value("Bank", bank, "plaid_access_token")
		account_id = None

	plaid = PlaidConnector(access_token)

	transactions = []
	try:
		transactions = plaid.get_transactions(start_date=start_date, end_date=end_date, account_id=account_id)
	except ItemError as e:
		if e.code == "ITEM_LOGIN_REQUIRED":
			msg = _("There was an error syncing transactions.") + " "
			msg += _("Please refresh or reset the Plaid linking of the Bank {}.").format(bank) + " "
			terminal_framework.log_error(message=msg, title=_("Plaid Link Refresh Required"))

	return transactions


def new_bank_transaction(transaction):
	result = []

	bank_account = terminal_framework.db.get_value("Bank Account", dict(integration_id=transaction["account_id"]))

	amount = float(transaction["amount"])
	if amount >= 0.0:
		deposit = 0.0
		withdrawal = amount
	else:
		deposit = abs(amount)
		withdrawal = 0.0

	tags = []
	if transaction["category"]:
		try:
			tags += transaction["category"]
			tags += [f'Plaid Cat. {transaction["category_id"]}']
		except KeyError:
			pass

	if not terminal_framework.db.exists(
		"Bank Transaction", dict(transaction_id=transaction["transaction_id"])
	) and not sbool(transaction["pending"]):
		try:
			new_transaction = terminal_framework.get_doc(
				{
					"doctype": "Bank Transaction",
					"date": getdate(transaction["date"]),
					"bank_account": bank_account,
					"deposit": deposit,
					"withdrawal": withdrawal,
					"currency": transaction["iso_currency_code"],
					"transaction_id": transaction["transaction_id"],
					"transaction_type": (
						transaction["transaction_code"] or transaction["payment_meta"]["payment_method"]
					),
					"reference_number": (
						transaction["check_number"]
						or transaction["payment_meta"]["reference_number"]
						or transaction["name"]
					),
					"description": transaction["name"],
				}
			)
			new_transaction.insert()
			new_transaction.submit()

			for tag in tags:
				add_tag(tag, "Bank Transaction", new_transaction.name)

			result.append(new_transaction.name)

		except Exception:
			terminal_framework.throw(_("Bank transaction creation error"))

	return result


def automatic_synchronization():
	settings = terminal_framework.get_doc("Plaid Settings", "Plaid Settings")
	if settings.enabled == 1 and settings.automatic_sync == 1:
		enqueue_synchronization()


@terminal_framework.whitelist()
def enqueue_synchronization():
	plaid_accounts = terminal_framework.get_all(
		"Bank Account", filters={"integration_id": ["!=", ""]}, fields=["name", "bank"]
	)

	for plaid_account in plaid_accounts:
		terminal_framework.enqueue(
			"terminal_erp.terminal_erp_integrations.doctype.plaid_settings.plaid_settings.sync_transactions",
			bank=plaid_account.bank,
			bank_account=plaid_account.name,
		)


@terminal_framework.whitelist()
def get_link_token_for_update(access_token: str):
	plaid = PlaidConnector(access_token)
	return plaid.get_link_token(update_mode=True)


def get_company(bank_account_name):
	from terminal_framework.defaults import get_user_default

	company_names = terminal_framework.db.get_all("Company", pluck="name")
	if len(company_names) == 1:
		return company_names[0]
	if terminal_framework.db.exists("Bank Account", bank_account_name):
		return terminal_framework.db.get_value("Bank Account", bank_account_name, "company")
	company_default = get_user_default("Company")
	if company_default:
		return company_default
	terminal_framework.throw(_("Could not detect the Company for updating Bank Accounts"))


@terminal_framework.whitelist()
def update_bank_account_ids(response: str | dict):
	data = terminal_framework.parse_json(response)
	institution_name = data["institution"]["name"]
	bank = terminal_framework.get_doc("Bank", institution_name).as_dict()
	bank_account_name = f"{data['account']['name']} - {institution_name}"
	return add_bank_accounts(response, bank, get_company(bank_account_name))
