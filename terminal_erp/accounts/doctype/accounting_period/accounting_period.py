# Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import terminal_framework
from terminal_framework import _
from terminal_framework.model.document import Document
from terminal_framework.utils import getdate, nowdate


class OverlapError(terminal_framework.ValidationError):
	pass


class ClosedAccountingPeriod(terminal_framework.ValidationError):
	pass


class AccountingPeriod(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.accounts.doctype.closed_document.closed_document import ClosedDocument

		closed_documents: DF.Table[ClosedDocument]
		company: DF.Link
		disabled: DF.Check
		end_date: DF.Date
		exempted_role: DF.Link | None
		period_name: DF.Data
		start_date: DF.Date
	# end: auto-generated types

	def validate(self):
		self.validate_dates()
		self.validate_overlap()

	def validate_dates(self):
		if getdate(self.start_date) > getdate(self.end_date):
			terminal_framework.throw(_("Start Date cannot be after End Date"))

		if getdate(self.end_date) > getdate(nowdate()):
			terminal_framework.throw(
				_(
					"Accounting Period cannot be created for a future date. End Date {0} is after today."
				).format(terminal_framework.bold(terminal_framework.format(self.end_date, "Date")))
			)

	def before_insert(self):
		self.bootstrap_doctypes_for_closing()

	def autoname(self):
		company_abbr = terminal_framework.get_cached_value("Company", self.company, "abbr")
		self.name = " - ".join([self.period_name, company_abbr])

	def validate_overlap(self):
		AccountingPeriod = terminal_framework.qb.DocType("Accounting Period")

		query = (
			terminal_framework.qb.from_(AccountingPeriod)
			.select(AccountingPeriod.name)
			.where(AccountingPeriod.start_date <= self.end_date)
			.where(AccountingPeriod.end_date >= self.start_date)
			.where(AccountingPeriod.name != self.name)
			.where(AccountingPeriod.company == self.company)
		)

		existing_accounting_period = query.run(as_dict=True)

		if len(existing_accounting_period) > 0:
			terminal_framework.throw(
				_("Accounting Period overlaps with {0}").format(existing_accounting_period[0].get("name")),
				OverlapError,
			)

	@terminal_framework.whitelist()
	def get_doctypes_for_closing(self):
		docs_for_closing = []
		# get period closing doctypes from all the apps
		doctypes = terminal_framework.get_hooks("period_closing_doctypes")

		closed_doctypes = [{"document_type": doctype, "closed": 1} for doctype in doctypes]
		for closed_doctype in closed_doctypes:
			docs_for_closing.append(closed_doctype)

		return docs_for_closing

	def bootstrap_doctypes_for_closing(self):
		if len(self.closed_documents) == 0:
			for doctype_for_closing in self.get_doctypes_for_closing():
				self.append(
					"closed_documents",
					{
						"document_type": doctype_for_closing.document_type,
						"closed": doctype_for_closing.closed,
					},
				)


def validate_accounting_period_on_doc_save(doc, method=None):
	if doc.doctype == "Bank Clearance":
		return
	elif doc.doctype == "Asset":
		if doc.asset_type == "Existing Asset":
			return
		else:
			date = doc.available_for_use_date
	elif doc.doctype == "Asset Repair":
		date = doc.completion_date
	elif doc.doctype == "Period Closing Voucher":
		date = doc.period_end_date
	else:
		date = doc.posting_date

	ap = terminal_framework.qb.DocType("Accounting Period")
	cd = terminal_framework.qb.DocType("Closed Document")

	accounting_period = (
		terminal_framework.qb.from_(ap)
		.from_(cd)
		.select(ap.name, ap.exempted_role)
		.where(
			(ap.name == cd.parent)
			& (ap.company == doc.company)
			& (ap.disabled == 0)
			& (cd.closed == 1)
			& (cd.document_type == doc.doctype)
			& (date >= ap.start_date)
			& (date <= ap.end_date)
		)
	).run(as_dict=1)

	if accounting_period:
		if (
			accounting_period[0].get("exempted_role")
			and accounting_period[0].get("exempted_role") in terminal_framework.get_roles()
		):
			return
		terminal_framework.throw(
			_("You cannot create a {0} within the closed Accounting Period {1}").format(
				doc.doctype, terminal_framework.bold(accounting_period[0]["name"])
			),
			ClosedAccountingPeriod,
		)
