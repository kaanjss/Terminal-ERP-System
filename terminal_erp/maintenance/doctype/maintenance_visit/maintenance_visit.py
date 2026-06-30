# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework
from terminal_framework import _
from terminal_framework.utils import format_date, get_datetime

from terminal_erp.utilities.transaction_base import TransactionBase


class MaintenanceVisit(TransactionBase):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.maintenance.doctype.maintenance_visit_purpose.maintenance_visit_purpose import (
			MaintenanceVisitPurpose,
		)

		address_display: DF.TextEditor | None
		amended_from: DF.Link | None
		company: DF.Link
		completion_status: DF.Literal["", "Partially Completed", "Fully Completed"]
		contact_display: DF.SmallText | None
		contact_email: DF.Data | None
		contact_mobile: DF.Data | None
		contact_person: DF.Link | None
		customer: DF.Link
		customer_address: DF.Link | None
		customer_feedback: DF.SmallText | None
		customer_group: DF.Link | None
		customer_name: DF.Data | None
		maintenance_schedule: DF.Link | None
		maintenance_schedule_detail: DF.Link | None
		maintenance_type: DF.Literal["", "Scheduled", "Unscheduled", "Breakdown"]
		mntc_date: DF.Date
		mntc_time: DF.Time | None
		naming_series: DF.Literal["MAT-MVS-.YYYY.-"]
		purposes: DF.Table[MaintenanceVisitPurpose]
		status: DF.Literal["", "Draft", "Cancelled", "Submitted"]
		territory: DF.Link | None
	# end: auto-generated types

	def validate_serial_no(self):
		for d in self.get("purposes"):
			if d.serial_no and not terminal_framework.db.exists("Serial No", d.serial_no):
				terminal_framework.throw(_("Serial No {0} does not exist").format(d.serial_no))

	def validate_purpose_table(self):
		if not self.purposes:
			terminal_framework.throw(_("Add Items in the Purpose Table"), title=_("Purposes Required"))

	def validate_maintenance_date(self):
		if self.maintenance_type == "Scheduled":
			if self.maintenance_schedule_detail:
				item_ref = terminal_framework.db.get_value(
					"Maintenance Schedule Detail", self.maintenance_schedule_detail, "item_reference"
				)
				if item_ref:
					start_date, end_date = terminal_framework.db.get_value(
						"Maintenance Schedule Item", item_ref, ["start_date", "end_date"]
					)
					if get_datetime(self.mntc_date) < get_datetime(start_date) or get_datetime(
						self.mntc_date
					) > get_datetime(end_date):
						terminal_framework.throw(
							_("Date must be between {0} and {1}").format(
								format_date(start_date), format_date(end_date)
							)
						)
			else:
				for purpose in self.purposes:
					if purpose.maintenance_schedule_detail:
						item_ref = terminal_framework.db.get_value(
							"Maintenance Schedule Detail",
							purpose.maintenance_schedule_detail,
							"item_reference",
						)
						if item_ref:
							start_date, end_date = terminal_framework.db.get_value(
								"Maintenance Schedule Item", item_ref, ["start_date", "end_date"]
							)
							if get_datetime(self.mntc_date) < get_datetime(start_date) or get_datetime(
								self.mntc_date
							) > get_datetime(end_date):
								terminal_framework.throw(
									_("Date must be between {0} and {1}").format(
										format_date(start_date), format_date(end_date)
									)
								)

	def validate(self):
		self.validate_serial_no()
		self.validate_maintenance_date()
		self.validate_purpose_table()

	def update_status_and_actual_date(self, cancel=False):
		status = "Pending"
		actual_date = None
		if not cancel:
			status = self.completion_status
			actual_date = self.mntc_date

		if self.maintenance_schedule_detail:
			terminal_framework.db.set_value(
				"Maintenance Schedule Detail", self.maintenance_schedule_detail, "completion_status", status
			)
			terminal_framework.db.set_value(
				"Maintenance Schedule Detail", self.maintenance_schedule_detail, "actual_date", actual_date
			)
		else:
			for purpose in self.purposes:
				if purpose.maintenance_schedule_detail:
					terminal_framework.db.set_value(
						"Maintenance Schedule Detail",
						purpose.maintenance_schedule_detail,
						"completion_status",
						status,
					)
					terminal_framework.db.set_value(
						"Maintenance Schedule Detail",
						purpose.maintenance_schedule_detail,
						"actual_date",
						actual_date,
					)

	def update_customer_issue(self, flag):
		if not self.maintenance_schedule:
			for d in self.get("purposes"):
				if d.prevdoc_docname and d.prevdoc_doctype == "Warranty Claim":
					if flag == 1:
						mntc_date = self.mntc_date
						service_person = d.service_person
						work_done = d.work_done
						status = "Open"
						if self.completion_status == "Fully Completed":
							status = "Closed"
						elif self.completion_status == "Partially Completed":
							status = "Work In Progress"
					else:
						mv = terminal_framework.qb.DocType("Maintenance Visit")
						mvp = terminal_framework.qb.DocType("Maintenance Visit Purpose")
						nm = (
							terminal_framework.qb.from_(mv)
							.inner_join(mvp)
							.on(mvp.parent == mv.name)
							.select(mv.name, mv.mntc_date, mvp.service_person, mvp.work_done)
							.where(
								(mv.completion_status == "Partially Completed")
								& (mvp.prevdoc_docname == d.prevdoc_docname)
								& (mv.name != self.name)
								& (mv.docstatus == 1)
							)
							.orderby(mv.name, order=terminal_framework.qb.desc)
							.limit(1)
							.run()
						)

						if nm:
							status = "Work In Progress"
							mntc_date = nm and nm[0][1] or ""
							service_person = nm and nm[0][2] or ""
							work_done = nm and nm[0][3] or ""
						else:
							status = "Open"
							mntc_date = None
							service_person = None
							work_done = None

					wc_doc = terminal_framework.get_doc("Warranty Claim", d.prevdoc_docname)
					wc_doc.update(
						{
							"resolution_date": mntc_date,
							"resolved_by": service_person,
							"resolution_details": work_done,
							"status": status,
						}
					)

					wc_doc.db_update()

	def check_if_last_visit(self):
		"""check if last maintenance visit against same sales order/ Warranty Claim"""
		check_for_docname = None
		for d in self.get("purposes"):
			if d.prevdoc_docname:
				check_for_docname = d.prevdoc_docname
				# check_for_doctype = d.prevdoc_doctype

		if check_for_docname:
			mv = terminal_framework.qb.DocType("Maintenance Visit")
			mvp = terminal_framework.qb.DocType("Maintenance Visit Purpose")
			check = (
				terminal_framework.qb.from_(mv)
				.inner_join(mvp)
				.on(mvp.parent == mv.name)
				.select(mv.name)
				.where(
					(mv.name != self.name)
					& (mvp.prevdoc_docname == check_for_docname)
					& (mv.docstatus == 1)
					& (
						(mv.mntc_date > self.mntc_date)
						| ((mv.mntc_date == self.mntc_date) & (mv.mntc_time > self.mntc_time))
					)
				)
				.run(pluck=True)
			)

			if check:
				check_lst = ",".join(check)
				terminal_framework.throw(
					_("Cancel Material Visits {0} before cancelling this Maintenance Visit").format(check_lst)
				)
				raise Exception
			else:
				self.update_customer_issue(0)

	def on_submit(self):
		self.update_customer_issue(1)
		self.db_set("status", "Submitted")
		self.update_status_and_actual_date()

	def on_cancel(self):
		self.check_if_last_visit()
		self.db_set("status", "Cancelled")
		self.update_status_and_actual_date(cancel=True)

	def on_update(self):
		pass
