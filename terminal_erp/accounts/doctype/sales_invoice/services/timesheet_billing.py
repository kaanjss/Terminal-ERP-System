# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

"""Timesheet billing helpers for Sales Invoice."""

import terminal_framework
from terminal_framework import _
from terminal_framework.utils import flt

from terminal_erp.projects.doctype.timesheet.timesheet import get_projectwise_timesheet_data


class TimesheetBillingService:
	def __init__(self, doc):
		self.doc = doc

	def validate_time_sheets_are_submitted(self) -> None:
		for data in self.doc.timesheets:
			if data.time_sheet and data.timesheet_detail:
				if sales_invoice := terminal_framework.db.get_value(
					"Timesheet Detail", data.timesheet_detail, "sales_invoice"
				):
					terminal_framework.throw(
						_("Row {0}: Sales Invoice {1} is already created for {2}").format(
							data.idx, terminal_framework.bold(sales_invoice), terminal_framework.bold(data.time_sheet)
						)
					)

			if data.time_sheet:
				status = terminal_framework.db.get_value("Timesheet", data.time_sheet, "status")
				if status not in ["Submitted", "Payslip", "Partially Billed"]:
					terminal_framework.throw(
						_("Timesheet {0} cannot be invoiced in its current state").format(data.time_sheet)
					)

	def update_time_sheet(self, sales_invoice: str | None) -> None:
		for d in self.doc.timesheets:
			if d.time_sheet:
				timesheet = terminal_framework.get_doc("Timesheet", d.time_sheet)
				self._update_time_sheet_detail(timesheet, d, sales_invoice)
				timesheet.calculate_total_amounts()
				timesheet.calculate_percentage_billed()
				timesheet.flags.ignore_validate_update_after_submit = True
				timesheet.set_status()
				timesheet.db_update_all()

	def unlink_sales_invoice_from_timesheets(self) -> None:
		for row in self.doc.timesheets:
			timesheet = terminal_framework.get_doc("Timesheet", row.time_sheet)
			timesheet.unlink_sales_invoice(self.doc.name)
			timesheet.flags.ignore_validate_update_after_submit = True
			timesheet.db_update_all()

	def set_billing_hours_and_amount(self) -> None:
		doc = self.doc
		if doc.project:
			return

		for timesheet in doc.timesheets:
			ts_doc = terminal_framework.get_doc("Timesheet", timesheet.time_sheet)
			if not timesheet.billing_hours and ts_doc.total_billable_hours:
				timesheet.billing_hours = ts_doc.total_billable_hours
			if not timesheet.billing_amount and ts_doc.total_billable_amount:
				timesheet.billing_amount = ts_doc.total_billable_amount

	def update_timesheet_billing_for_project(self) -> None:
		doc = self.doc
		if (
			not doc.is_return
			and not doc.timesheets
			and doc.project
			and terminal_framework.db.get_single_value("Projects Settings", "fetch_timesheet_in_sales_invoice")
		):
			self.add_timesheet_data()
		else:
			self.calculate_billing_amount_for_timesheet()

	def add_timesheet_data(self) -> None:
		doc = self.doc
		doc.set("timesheets", [])
		if doc.project:
			for data in get_projectwise_timesheet_data(doc.project):
				doc.append(
					"timesheets",
					{
						"time_sheet": data.time_sheet,
						"billing_hours": data.billing_hours,
						"billing_amount": data.billing_amount,
						"timesheet_detail": data.name,
						"activity_type": data.activity_type,
						"description": data.description,
					},
				)
			self.calculate_billing_amount_for_timesheet()

	def calculate_billing_amount_for_timesheet(self) -> None:
		doc = self.doc
		doc.total_billing_amount = sum(flt(ts.billing_amount) for ts in doc.timesheets)
		doc.total_billing_hours = sum(flt(ts.billing_hours) for ts in doc.timesheets)

	def _update_time_sheet_detail(self, timesheet, args, sales_invoice: str | None) -> None:
		for data in timesheet.time_logs:
			if args.timesheet_detail == data.name and self._should_set_sales_invoice(data, sales_invoice):
				data.sales_invoice = sales_invoice

	def _should_set_sales_invoice(self, time_log, sales_invoice: str | None) -> bool:
		"""Whether this time log's sales-invoice link should be (re)set to sales_invoice."""
		doc = self.doc
		if doc.project:
			return True
		if not time_log.sales_invoice:
			return True
		if not sales_invoice and time_log.sales_invoice == doc.name:
			# clearing the link on cancellation of this invoice
			return True
		# clearing the link on a return raised against the original invoice
		return bool(
			doc.is_return
			and doc.return_against
			and not sales_invoice
			and time_log.sales_invoice == doc.return_against
		)
