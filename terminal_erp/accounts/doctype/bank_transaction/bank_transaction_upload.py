# Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import json

import terminal_framework
from terminal_framework.utils import getdate
from terminal_framework.utils.dateutils import parse_date


@terminal_framework.whitelist()
def upload_bank_statement():
	if getattr(terminal_framework, "uploaded_file", None):
		with open(terminal_framework.uploaded_file, "rb") as upfile:
			fcontent = upfile.read()
	else:
		fcontent = terminal_framework.local.uploaded_file
		fname = terminal_framework.local.uploaded_filename

	if terminal_framework.safe_encode(fname).lower().endswith(b"csv"):
		from terminal_framework.utils.csvutils import read_csv_content

		rows = read_csv_content(fcontent, False)

	elif terminal_framework.safe_encode(fname).lower().endswith(b"xlsx"):
		from terminal_framework.utils.xlsxutils import read_xlsx_file_from_attached_file

		rows = read_xlsx_file_from_attached_file(fcontent=fcontent)

	columns = rows[0]
	rows.pop(0)
	data = rows
	return {"columns": columns, "data": data}


@terminal_framework.whitelist()
def create_bank_entries(columns: str, data: str | list, bank_account: str):
	header_map = get_header_mapping(columns, bank_account)

	success = 0
	errors = 0
	for d in terminal_framework.parse_json(data):
		if all(item is None for item in d) is True:
			continue
		fields = {}
		for key, value in header_map.items():
			fields.update({key: d[int(value) - 1]})

		terminal_framework.db.savepoint("bank_entry")
		try:
			bank_transaction = terminal_framework.get_doc({"doctype": "Bank Transaction"})
			bank_transaction.update(fields)
			bank_transaction.date = getdate(parse_date(bank_transaction.date))
			bank_transaction.bank_account = bank_account
			bank_transaction.insert()
			bank_transaction.submit()
			success += 1
		except Exception:
			terminal_framework.db.rollback(save_point="bank_entry")
			terminal_framework.log_error(title="Bank entry creation failed")
			errors += 1

	return {"success": success, "errors": errors}


def get_header_mapping(columns, bank_account):
	mapping = get_bank_mapping(bank_account)

	header_map = {}
	for column in terminal_framework.parse_json(columns):
		if column["content"] in mapping:
			header_map.update({mapping[column["content"]]: column["colIndex"]})

	return header_map


def get_bank_mapping(bank_account):
	bank_name = terminal_framework.get_cached_value("Bank Account", bank_account, "bank")
	bank = terminal_framework.get_doc("Bank", bank_name)

	mapping = {row.file_field: row.bank_transaction_field for row in bank.bank_transaction_mapping}

	return mapping
