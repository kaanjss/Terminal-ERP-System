# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from collections import defaultdict
from itertools import chain

import terminal_framework
from terminal_framework import _
from terminal_framework.query_builder import Interval
from terminal_framework.query_builder.functions import Count, CurDate, UnixTimestamp
from terminal_framework.utils import flt
from terminal_framework.utils.data import get_url_to_list
from terminal_framework.utils.nestedset import NestedSet, get_root_of

from terminal_erp import get_default_currency


class SalesPerson(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.setup.doctype.target_detail.target_detail import TargetDetail

		commission_rate: DF.Data | None
		department: DF.Link | None
		employee: DF.Link | None
		enabled: DF.Check
		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Data | None
		parent_sales_person: DF.Link | None
		rgt: DF.Int
		sales_person_name: DF.Data
		targets: DF.Table[TargetDetail]
	# end: auto-generated types

	nsm_parent_field = "parent_sales_person"

	def validate(self):
		if not self.enabled:
			self.validate_sales_person()

		if not self.parent_sales_person:
			self.parent_sales_person = get_root_of("Sales Person")

		for d in self.get("targets") or []:
			if not flt(d.target_qty) and not flt(d.target_amount):
				terminal_framework.throw(_("Either target qty or target amount is mandatory."))
		self.validate_employee_id()

	def onload(self):
		self.load_dashboard_info()

	def load_dashboard_info(self):
		company_default_currency = get_default_currency()

		allocated_amount_against_order = flt(
			terminal_framework.db.get_value(
				"Sales Team",
				{"docstatus": 1, "parenttype": "Sales Order", "sales_person": self.sales_person_name},
				[{"SUM": "allocated_amount"}],
			)
		)

		allocated_amount_against_invoice = flt(
			terminal_framework.db.get_value(
				"Sales Team",
				{"docstatus": 1, "parenttype": "Sales Invoice", "sales_person": self.sales_person_name},
				[{"SUM": "allocated_amount"}],
			)
		)

		info = {}
		info["allocated_amount_against_order"] = allocated_amount_against_order
		info["allocated_amount_against_invoice"] = allocated_amount_against_invoice
		info["currency"] = company_default_currency

		self.set_onload("dashboard_info", info)

	def on_update(self):
		super().on_update()
		self.validate_one_root()

	def validate_sales_person(self):
		sales_team = terminal_framework.qb.DocType("Sales Team")

		query = (
			terminal_framework.qb.from_(sales_team)
			.select(sales_team.sales_person)
			.where((sales_team.sales_person == self.name) & (sales_team.parenttype == "Customer"))
			.groupby(sales_team.sales_person)
		).run(as_dict=True)

		if query:
			terminal_framework.throw(
				_("The Sales Person is linked with {0}").format(
					terminal_framework.bold(
						f"""<a href="{get_url_to_list("Customer")}?sales_person={self.name}">{"Customers"}</a>"""
					)
				)
			)

	def get_email_id(self):
		if self.employee:
			user = terminal_framework.db.get_value("Employee", self.employee, "user_id")
			if not user:
				terminal_framework.throw(_("User ID not set for Employee {0}").format(self.employee))
			else:
				return terminal_framework.db.get_value("User", user, "email") or user

	def validate_employee_id(self):
		if self.employee:
			sales_person = terminal_framework.db.get_value("Sales Person", {"employee": self.employee})

			if sales_person and sales_person != self.name:
				terminal_framework.throw(
					_("Another Sales Person {0} exists with the same Employee id").format(sales_person)
				)


def on_doctype_update():
	terminal_framework.db.add_index("Sales Person", ["lft", "rgt"])


def get_timeline_data(doctype: str, name: str) -> dict[int, int]:
	def _fetch_activity(doctype: str, date_field: str):
		sales_team = terminal_framework.qb.DocType("Sales Team")
		transaction = terminal_framework.qb.DocType(doctype)

		return dict(
			terminal_framework.qb.from_(transaction)
			.join(sales_team)
			.on(transaction.name == sales_team.parent)
			.select(UnixTimestamp(transaction[date_field]), Count("*"))
			.where(sales_team.sales_person == name)
			.where(transaction[date_field] > CurDate() - Interval(years=1))
			.groupby(transaction[date_field])
			.run()
		)

	sales_order_activity = _fetch_activity("Sales Order", "transaction_date")
	sales_invoice_activity = _fetch_activity("Sales Invoice", "posting_date")
	delivery_note_activity = _fetch_activity("Delivery Note", "posting_date")

	merged_activities = defaultdict(int)

	for ts, count in chain(
		sales_order_activity.items(), sales_invoice_activity.items(), delivery_note_activity.items()
	):
		merged_activities[ts] += count

	return merged_activities
