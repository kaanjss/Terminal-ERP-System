# Copyright (c) 2020, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import terminal_framework
from terminal_framework import _
from terminal_framework.utils import cint, get_link_to_form

from terminal_erp.controllers.status_updater import StatusUpdater


class POSOpeningEntry(StatusUpdater):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.accounts.doctype.pos_opening_entry_detail.pos_opening_entry_detail import (
			POSOpeningEntryDetail,
		)

		amended_from: DF.Link | None
		balance_details: DF.Table[POSOpeningEntryDetail]
		company: DF.Link
		period_end_date: DF.Date | None
		period_start_date: DF.Datetime
		pos_closing_entry: DF.Data | None
		pos_profile: DF.Link
		posting_date: DF.Date
		set_posting_date: DF.Check
		status: DF.Literal["Draft", "Open", "Closed", "Cancelled"]
		user: DF.Link
	# end: auto-generated types

	def validate(self):
		self.validate_pos_profile_and_cashier()
		self.check_open_pos_exists()
		self.check_user_already_assigned()
		self.validate_payment_method_account()
		self.set_status()

	def validate_pos_profile_and_cashier(self):
		if not terminal_framework.db.exists("POS Profile", self.pos_profile):
			terminal_framework.throw(_("POS Profile {0} does not exist.").format(self.pos_profile))

		pos_profile_company, pos_profile_disabled = terminal_framework.db.get_value(
			"POS Profile", self.pos_profile, ["company", "disabled"]
		)

		if pos_profile_disabled:
			terminal_framework.throw(_("POS Profile {0} is disabled.").format(terminal_framework.bold(self.pos_profile)))

		if self.company != pos_profile_company:
			terminal_framework.throw(
				_("POS Profile {0} does not belong to company {1}").format(self.pos_profile, self.company)
			)

		if not cint(terminal_framework.db.get_value("User", self.user, "enabled")):
			terminal_framework.throw(_("User {0} is disabled. Please select valid user/cashier").format(self.user))

	def check_open_pos_exists(self):
		if terminal_framework.db.exists("POS Opening Entry", {"pos_profile": self.pos_profile, "status": "Open"}):
			terminal_framework.throw(
				title=_("POS Opening Entry Exists"),
				msg=_(
					"{0} is open. Close the POS or cancel the existing POS Opening Entry to create a new POS Opening Entry."
				).format(terminal_framework.bold(self.pos_profile)),
			)

	def check_user_already_assigned(self):
		if terminal_framework.db.exists("POS Opening Entry", {"user": self.user, "status": "Open"}):
			terminal_framework.throw(
				title=_("Cannot Assign Cashier"),
				msg=_("Cashier is currently assigned to another POS."),
			)

	def validate_payment_method_account(self):
		invalid_modes = []
		for d in self.balance_details:
			if d.mode_of_payment:
				account = terminal_framework.db.get_value(
					"Mode of Payment Account",
					{"parent": d.mode_of_payment, "company": self.company},
					"default_account",
				)
				if not account:
					invalid_modes.append(get_link_to_form("Mode of Payment", d.mode_of_payment))

		if invalid_modes:
			if invalid_modes == 1:
				msg = _("Please set default Cash or Bank account in Mode of Payment {0}")
			else:
				msg = _("Please set default Cash or Bank account in Mode of Payments {0}")
			terminal_framework.throw(msg.format(", ".join(invalid_modes)), title=_("Missing Account"))

	def on_submit(self):
		self.set_status(update=True)

	def before_cancel(self):
		self.check_poe_is_cancellable()

	def on_cancel(self):
		self.set_status(update=True)
		terminal_framework.publish_realtime(
			f"poe_{self.name}",
			message={"operation": "Cancelled"},
			docname=f"POS Opening Entry/{self.name}",
		)

	def check_poe_is_cancellable(self):
		from terminal_erp.accounts.doctype.pos_closing_entry.pos_closing_entry import get_invoices

		invoices = get_invoices(
			self.period_start_date, terminal_framework.utils.get_datetime(), self.pos_profile, self.user
		)
		if invoices.get("invoices"):
			terminal_framework.throw(
				title=_("POS Opening Entry Cancellation Error"),
				msg=_("POS Opening Entry cannot be cancelled as unconsolidated Invoices exists."),
			)
