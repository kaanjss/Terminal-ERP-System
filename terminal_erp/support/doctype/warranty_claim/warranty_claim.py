# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework
from terminal_framework import _, session
from terminal_framework.model.document import Document
from terminal_framework.utils import now_datetime

from terminal_erp.utilities.transaction_base import TransactionBase


class WarrantyClaim(TransactionBase):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		address_display: DF.TextEditor | None
		amc_expiry_date: DF.Date | None
		amended_from: DF.Link | None
		company: DF.Link
		complaint: DF.TextEditor
		complaint_date: DF.Date
		complaint_raised_by: DF.Data | None
		contact_display: DF.SmallText | None
		contact_email: DF.Data | None
		contact_mobile: DF.Data | None
		contact_person: DF.Link | None
		customer: DF.Link
		customer_address: DF.Link | None
		customer_group: DF.Link | None
		customer_name: DF.Data | None
		description: DF.SmallText | None
		from_company: DF.Data | None
		item_code: DF.Link | None
		item_name: DF.Data | None
		naming_series: DF.Literal["SER-WRN-.YYYY.-"]
		resolution_date: DF.Datetime | None
		resolution_details: DF.Text | None
		resolved_by: DF.Link | None
		serial_no: DF.Link | None
		service_address: DF.SmallText | None
		status: DF.Literal["", "Open", "Closed", "Work In Progress", "Cancelled"]
		territory: DF.Link | None
		warranty_amc_status: DF.Literal["", "Under Warranty", "Out of Warranty", "Under AMC", "Out of AMC"]
		warranty_expiry_date: DF.Date | None
	# end: auto-generated types

	def validate(self):
		if session["user"] != "Guest" and not self.customer:
			terminal_framework.throw(_("Customer is required"))

		if (
			self.status == "Closed"
			and not self.resolution_date
			and terminal_framework.db.get_value("Warranty Claim", self.name, "status") != "Closed"
		):
			self.resolution_date = now_datetime()

	def on_cancel(self):
		mv = terminal_framework.qb.DocType("Maintenance Visit")
		mvp = terminal_framework.qb.DocType("Maintenance Visit Purpose")
		# filter the parent Maintenance Visit's docstatus (as the original SQL did), not the child row's
		visits = (
			terminal_framework.qb.from_(mvp)
			.inner_join(mv)
			.on(mvp.parent == mv.name)
			.select(mv.name)
			.where((mvp.prevdoc_docname == self.name) & (mv.docstatus != 2))
			.limit(500)
			.run()
		)
		if visits:
			lst1 = ",".join(x[0] for x in visits)
			terminal_framework.throw(_("Cancel Material Visit {0} before cancelling this Warranty Claim").format(lst1))
		else:
			self.db_set("status", "Cancelled")

	def on_update(self):
		pass


@terminal_framework.whitelist()
def make_maintenance_visit(source_name: str, target_doc: str | Document | None = None):
	from terminal_framework.model.mapper import get_mapped_doc, map_child_doc

	def _update_links(source_doc, target_doc, source_parent):
		target_doc.prevdoc_doctype = source_parent.doctype
		target_doc.prevdoc_docname = source_parent.name

	mv = terminal_framework.qb.DocType("Maintenance Visit")
	mvp = terminal_framework.qb.DocType("Maintenance Visit Purpose")
	visit = (
		terminal_framework.qb.from_(mv)
		.inner_join(mvp)
		.on(mvp.parent == mv.name)
		.select(mv.name)
		.where(
			(mvp.prevdoc_docname == source_name)
			& (mv.docstatus == 1)
			& (mv.completion_status == "Fully Completed")
		)
		.run()
	)

	if not visit:
		target_doc = get_mapped_doc(
			"Warranty Claim",
			source_name,
			{"Warranty Claim": {"doctype": "Maintenance Visit", "field_map": {}}},
			target_doc,
		)

		source_doc = terminal_framework.get_doc("Warranty Claim", source_name)
		if source_doc.get("item_code"):
			table_map = {"doctype": "Maintenance Visit Purpose", "postprocess": _update_links}
			map_child_doc(source_doc, target_doc, table_map, source_doc)

		return target_doc
