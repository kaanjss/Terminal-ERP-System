# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import json
import os

import terminal_framework
from terminal_framework import _
from terminal_framework.model.document import Document, bulk_insert

DOCTYPE = "Account Category"


class AccountCategory(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		account_category_name: DF.Data
		description: DF.SmallText | None
		root_type: DF.Literal["", "Asset", "Liability", "Income", "Expense", "Equity"]
	# end: auto-generated types

	def after_rename(self, old_name, new_name, merge):
		from terminal_erp.accounts.doctype.financial_report_template.financial_report_engine import (
			FormulaFieldUpdater,
		)

		# get all template rows with this account category being used
		row = terminal_framework.qb.DocType("Financial Report Row")
		rows = terminal_framework._dict(
			terminal_framework.qb.from_(row)
			.select(row.name, row.calculation_formula)
			.where(row.calculation_formula.like(f"%{old_name}%"))
			.run()
		)

		if not rows:
			return

		# Update formulas with new name
		updater = FormulaFieldUpdater(
			field_name="account_category",
			value_mapping={old_name: new_name},
			exclude_operators=["like", "not like"],
		)

		updated_formulas = updater.update_in_rows(rows)

		if updated_formulas:
			terminal_framework.msgprint(
				_("Updated {0} Financial Report Row(s) with new category name").format(len(updated_formulas))
			)


def import_account_categories(template_path: str):
	categories_file = os.path.join(template_path, "account_categories.json")

	if not os.path.exists(categories_file):
		return

	with open(categories_file) as f:
		categories = json.load(f, object_hook=terminal_framework._dict)

	create_account_categories(categories)


def create_account_categories(categories: list[dict]):
	if not categories:
		return

	existing_categories = set(terminal_framework.get_all(DOCTYPE, pluck="name"))
	new_categories = []

	for category_data in categories:
		category_name = category_data.get("account_category_name")
		if not category_name or category_name in existing_categories:
			continue

		doc = terminal_framework.get_doc(
			{
				**category_data,
				"doctype": DOCTYPE,
				"name": category_name,
			}
		)

		new_categories.append(doc)
		existing_categories.add(category_name)

	if new_categories:
		bulk_insert(DOCTYPE, new_categories)
