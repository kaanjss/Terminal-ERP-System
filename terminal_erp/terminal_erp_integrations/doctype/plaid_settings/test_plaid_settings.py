# Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt
import json

import terminal_framework
from terminal_framework.utils.response import json_handler

from terminal_erp.terminal_erp_integrations.doctype.plaid_settings.plaid_settings import (
	add_account_subtype,
	add_account_type,
	add_bank_accounts,
	get_plaid_configuration,
	new_bank_transaction,
)
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestPlaidSettings(Terminal ERPTestSuite):
	def test_plaid_disabled(self):
		terminal_framework.db.set_single_value("Plaid Settings", "enabled", 0)
		self.assertEqual(get_plaid_configuration(), "disabled")

	def test_add_account_type(self):
		add_account_type("brokerage")
		self.assertEqual(terminal_framework.get_doc("Bank Account Type", "brokerage").name, "brokerage")

	def test_add_account_subtype(self):
		add_account_subtype("loan")
		self.assertEqual(terminal_framework.get_doc("Bank Account Subtype", "loan").name, "loan")

	def test_new_transaction(self):
		if not terminal_framework.db.exists("Bank", "Citi"):
			terminal_framework.get_doc({"doctype": "Bank", "bank_name": "Citi"}).insert()

		bank_accounts = {
			"account": {
				"subtype": "checking",
				"mask": "0000",
				"type": "depository",
				"id": "6GbM6RRQgdfy3lAqGz4JUnpmR948WZFg8DjQK",
				"name": "Plaid Checking",
			},
			"account_id": "6GbM6RRQgdfy3lAqGz4JUnpmR948WZFg8DjQK",
			"link_session_id": "db673d75-61aa-442a-864f-9b3f174f3725",
			"accounts": [
				{
					"type": "depository",
					"subtype": "checking",
					"mask": "0000",
					"id": "6GbM6RRQgdfy3lAqGz4JUnpmR948WZFg8DjQK",
					"name": "Plaid Checking",
				}
			],
			"institution": {"institution_id": "ins_6", "name": "Citi"},
		}

		bank = json.dumps(terminal_framework.get_doc("Bank", "Citi").as_dict(), default=json_handler)
		company = "_Test Company"

		add_bank_accounts(bank_accounts, bank, company)

		transactions = {
			"account_owner": None,
			"category": ["Food and Drink", "Restaurants"],
			"account_id": "b4Jkp1LJDZiPgojpr1ansXJrj5Q6w9fVmv6ov",
			"pending_transaction_id": None,
			"transaction_id": "x374xPa7DvUewqlR5mjNIeGK8r8rl3Sn647LM",
			"unofficial_currency_code": None,
			"name": "INTRST PYMNT",
			"transaction_type": "place",
			"transaction_code": "direct debit",
			"check_number": "3456789",
			"amount": -4.22,
			"location": {
				"city": None,
				"zip": None,
				"store_number": None,
				"lon": None,
				"state": None,
				"address": None,
				"lat": None,
			},
			"payment_meta": {
				"reference_number": None,
				"payer": None,
				"payment_method": None,
				"reason": None,
				"payee": None,
				"ppd_id": None,
				"payment_processor": None,
				"by_order_of": None,
			},
			"date": "2017-12-22",
			"category_id": "13005000",
			"pending": False,
			"iso_currency_code": "USD",
		}

		new_bank_transaction(transactions)

		self.assertEqual(len(terminal_framework.get_all("Bank Transaction")), 1)
