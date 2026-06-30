# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import terminal_framework
from terminal_framework import _
from terminal_framework.contacts.doctype.contact.contact import get_full_name
from terminal_framework.core.doctype.communication.email import make
from terminal_framework.desk.form.load import get_attachments
from terminal_framework.model.document import Document
from terminal_framework.query_builder import Order
from terminal_framework.utils import get_url
from terminal_framework.utils.print_format import download_pdf
from terminal_framework.utils.user import get_user_fullname

from terminal_erp.buying.utils import validate_for_items
from terminal_erp.controllers.buying_controller import BuyingController

STANDARD_USERS = ("Guest", "Administrator")


class RequestforQuotation(BuyingController):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.buying.doctype.request_for_quotation_item.request_for_quotation_item import (
			RequestforQuotationItem,
		)
		from terminal_erp.buying.doctype.request_for_quotation_supplier.request_for_quotation_supplier import (
			RequestforQuotationSupplier,
		)

		amended_from: DF.Link | None
		billing_address: DF.Link | None
		billing_address_display: DF.TextEditor | None
		company: DF.Link
		email_template: DF.Link | None
		has_unit_price_items: DF.Check
		incoterm: DF.Link | None
		items: DF.Table[RequestforQuotationItem]
		letter_head: DF.Link | None
		message_for_supplier: DF.TextEditor | None
		mfs_html: DF.Code | None
		named_place: DF.Data | None
		naming_series: DF.Literal["PUR-RFQ-.YYYY.-"]
		opportunity: DF.Link | None
		schedule_date: DF.Date | None
		select_print_heading: DF.Link | None
		send_attached_files: DF.Check
		send_document_print: DF.Check
		shipping_address: DF.Link | None
		shipping_address_display: DF.TextEditor | None
		status: DF.Literal["", "Draft", "Submitted", "Cancelled"]
		subject: DF.Data
		suppliers: DF.Table[RequestforQuotationSupplier]
		tc_name: DF.Link | None
		terms: DF.TextEditor | None
		title: DF.Data | None
		transaction_date: DF.Date
		use_html: DF.Check
		vendor: DF.Link | None
	# end: auto-generated types

	def before_validate(self):
		self.set_has_unit_price_items()
		self.flags.allow_zero_qty = self.has_unit_price_items
		self.set_data_for_supplier()

	def validate(self):
		self.validate_duplicate_supplier()
		self.validate_supplier_list()
		super().validate_qty_is_not_zero()
		validate_for_items(self)
		super().set_qty_as_per_stock_uom()
		self.update_email_id()

		if self.docstatus < 1:
			# after amend and save, status still shows as cancelled, until submit
			self.db_set("status", "Draft")

	def set_has_unit_price_items(self):
		"""
		If permitted in settings and any item has 0 qty, the RFQ has unit price items.
		"""
		if not terminal_framework.db.get_single_value("Buying Settings", "allow_zero_qty_in_request_for_quotation"):
			return

		self.has_unit_price_items = any(
			not row.qty for row in self.get("items") if (row.item_code and not row.qty)
		)

	def set_data_for_supplier(self):
		if self.email_template:
			data = terminal_framework.get_value(
				"Email Template",
				self.email_template,
				["use_html", "response", "response_html", "subject"],
				as_dict=True,
			)

			self.use_html = data.use_html

			if data.use_html:
				if not self.mfs_html:
					self.mfs_html = data.response_html
			else:
				if not self.message_for_supplier:
					self.message_for_supplier = data.response

			if not self.subject:
				self.subject = data.subject

	def validate_duplicate_supplier(self):
		supplier_list = [d.supplier for d in self.suppliers]
		if len(supplier_list) != len(set(supplier_list)):
			terminal_framework.throw(_("Same supplier has been entered multiple times"))

	def validate_supplier_list(self):
		for d in self.suppliers:
			prevent_rfqs = terminal_framework.db.get_value("Supplier", d.supplier, "prevent_rfqs")
			if prevent_rfqs:
				standing = terminal_framework.db.get_value("Supplier Scorecard", d.supplier, "status")
				terminal_framework.throw(
					_("RFQs are not allowed for {0} due to a scorecard standing of {1}").format(
						d.supplier, standing
					)
				)
			warn_rfqs = terminal_framework.db.get_value("Supplier", d.supplier, "warn_rfqs")
			if warn_rfqs:
				standing = terminal_framework.db.get_value("Supplier Scorecard", d.supplier, "status")
				terminal_framework.msgprint(
					_(
						"{0} currently has a {1} Supplier Scorecard standing, and RFQs to this supplier should be issued with caution."
					).format(d.supplier, standing),
					title=_("Caution"),
					indicator="orange",
				)

	def update_email_id(self):
		for rfq_supplier in self.suppliers:
			if not rfq_supplier.email_id:
				rfq_supplier.email_id = terminal_framework.db.get_value("Contact", rfq_supplier.contact, "email_id")

	def validate_email_id(self, args):
		if not args.email_id:
			terminal_framework.throw(
				_("Row {0}: For Supplier {1}, Email Address is Required to send an email").format(
					args.idx, terminal_framework.bold(args.supplier)
				)
			)

	def on_submit(self):
		self.db_set("status", "Submitted")
		for supplier in self.suppliers:
			supplier.email_sent = 0
			supplier.quote_status = "Pending"
		self.send_to_supplier()

	def before_print(self, settings=None):
		"""Use the first suppliers data to render the print preview."""
		if self.vendor or not self.suppliers:
			# If a specific supplier is already set, via Tools > Download PDF,
			# we don't want to override it.
			return

		self.update_supplier_part_no(self.suppliers[0].supplier)

	def on_cancel(self):
		self.db_set("status", "Cancelled")

	@terminal_framework.whitelist()
	def get_supplier_email_preview(self, supplier: str):
		"""Returns formatted email preview as string."""
		rfq_suppliers = list(filter(lambda row: row.supplier == supplier, self.suppliers))
		rfq_supplier = rfq_suppliers[0]

		self.validate_email_id(rfq_supplier)

		message = self.supplier_rfq_mail(rfq_supplier, "", self.get_link(), True)

		return message

	def send_to_supplier(self):
		"""Sends RFQ mail to involved suppliers."""
		for rfq_supplier in self.suppliers:
			if rfq_supplier.email_id is not None and rfq_supplier.send_email:
				self.validate_email_id(rfq_supplier)

				# make new user if required
				update_password_link, contact = self.update_supplier_contact(rfq_supplier, self.get_link())

				self.update_supplier_part_no(rfq_supplier.supplier)
				self.supplier_rfq_mail(rfq_supplier, update_password_link, self.get_link())
				rfq_supplier.email_sent = 1
				if not rfq_supplier.contact:
					rfq_supplier.contact = contact
				rfq_supplier.save()

	def get_link(self):
		# RFQ link for supplier portal
		route = terminal_framework.db.get_value(
			"Portal Menu Item", {"reference_doctype": "Request for Quotation"}, ["route"]
		)
		if not route:
			terminal_framework.throw(_("Please add Request for Quotation to the sidebar in Portal Settings."))

		return get_url(f"{route}/{self.name}")

	def update_supplier_part_no(self, supplier):
		self.vendor = supplier
		for item in self.items:
			item.supplier_part_no = terminal_framework.db.get_value(
				"Item Supplier", {"parent": item.item_code, "supplier": supplier}, "supplier_part_no"
			)

	def update_supplier_contact(self, rfq_supplier, link):
		"""Create a new user for the supplier if not set in contact"""
		update_password_link, contact = "", ""

		if terminal_framework.db.exists("User", rfq_supplier.email_id):
			user = terminal_framework.get_doc("User", rfq_supplier.email_id)
		else:
			user, update_password_link = self.create_user(rfq_supplier, link)

		contact = self.link_supplier_contact(rfq_supplier, user)

		return update_password_link, contact

	def link_supplier_contact(self, rfq_supplier, user):
		"""If no Contact, create a new contact against Supplier. If Contact exists, check if email and user id set."""
		if rfq_supplier.contact:
			contact = terminal_framework.get_doc("Contact", rfq_supplier.contact)
		else:
			contact = terminal_framework.new_doc("Contact")
			contact.first_name = rfq_supplier.supplier_name or rfq_supplier.supplier
			contact.append("links", {"link_doctype": "Supplier", "link_name": rfq_supplier.supplier})
			contact.append("email_ids", {"email_id": user.name, "is_primary": 1})

		if not contact.email_id and not contact.user:
			contact.email_id = user.name
			contact.user = user.name

		contact.save(ignore_permissions=True)

		if rfq_supplier.supplier:
			self.update_user_in_supplier(rfq_supplier.supplier, user.name)

		if not rfq_supplier.contact:
			# return contact to later update, RFQ supplier row's contact
			return contact.name

	def update_user_in_supplier(self, supplier, user):
		"""Update user in Supplier."""
		if not terminal_framework.db.exists("Portal User", {"parent": supplier, "user": user}):
			supplier_doc = terminal_framework.get_doc("Supplier", supplier)
			supplier_doc.append(
				"portal_users",
				{
					"user": user,
				},
			)

			supplier_doc.flags.ignore_validate = True
			supplier_doc.flags.ignore_mandatory = True
			supplier_doc.flags.ignore_permissions = True

			supplier_doc.save()

	def create_user(self, rfq_supplier, link):
		contact_name = None
		if rfq_supplier.contact:
			name_fields = terminal_framework.get_value(
				"Contact", rfq_supplier.contact, ["first_name", "middle_name", "last_name"]
			)
			if name_fields:
				contact_name = get_full_name(*name_fields)

		user = terminal_framework.get_doc(
			{
				"doctype": "User",
				"send_welcome_email": 0,
				"email": rfq_supplier.email_id,
				"first_name": contact_name or rfq_supplier.supplier_name or rfq_supplier.supplier,
				"user_type": "Website User",
				"redirect_url": link,
			}
		)
		user.save(ignore_permissions=True)
		update_password_link = user._reset_password()

		return user, update_password_link

	def supplier_rfq_mail(self, data, update_password_link, rfq_link, preview=False):
		full_name = get_user_fullname(terminal_framework.session["user"])
		if full_name == "Guest":
			full_name = "Administrator"

		doc_args = self.as_dict()

		if data.get("contact"):
			contact = terminal_framework.get_doc("Contact", data.get("contact"))
			doc_args["contact"] = contact.as_dict()

		doc_args.update(
			{
				"supplier": data.get("supplier"),
				"supplier_name": data.get("supplier_name"),
				"update_password_link": f'<a href="{update_password_link}" class="btn btn-default btn-xs" target="_blank">{_("Set Password")}</a>',
				"portal_link": f'<a href="{rfq_link}" class="btn btn-default btn-xs" target="_blank"> {_("Submit your Quotation")} </a>',
				"user_fullname": full_name,
			}
		)

		fixed_procurement_email = terminal_framework.db.get_single_value("Buying Settings", "fixed_email")
		if fixed_procurement_email:
			sender = terminal_framework.db.get_value("Email Account", fixed_procurement_email, "email_id")
		else:
			sender = terminal_framework.session.user not in STANDARD_USERS and terminal_framework.session.user or None

		message_template = self.mfs_html if self.use_html else self.message_for_supplier
		# nosemgrep: terminal_framework-semgrep-rules.rules.security.terminal_framework-ssti
		rendered_message = terminal_framework.render_template(message_template, doc_args)

		subject_source = (
			self.subject
			or terminal_framework.get_value("Email Template", self.email_template, "subject")
			or _("Request for Quotation")
		)
		rendered_subject = terminal_framework.render_template(subject_source, doc_args)
		if preview:
			return {
				"message": rendered_message,
				"subject": rendered_subject,
			}

		attachments = []
		if self.send_attached_files:
			attachments = self.get_attachments()

		if self.send_document_print:
			supplier_language = terminal_framework.db.get_value("Supplier", data.supplier, "language")
			system_language = terminal_framework.db.get_single_value("System Settings", "language")
			attachments.append(
				terminal_framework.attach_print(
					self.doctype,
					self.name,
					doc=self,
					print_format=self.meta.default_print_format or "Standard",
					lang=supplier_language or system_language,
					letterhead=self.letter_head,
				)
			)

		self.send_email(
			data,
			sender,
			rendered_subject,
			rendered_message,
			attachments,
		)

	def send_email(self, data, sender, subject, message, attachments):
		make(
			subject=subject,
			content=message,
			recipients=data.email_id,
			sender=sender,
			attachments=attachments,
			send_email=True,
			doctype=self.doctype,
			name=self.name,
		)["name"]

		terminal_framework.msgprint(_("Email Sent to Supplier {0}").format(data.supplier))

	def get_attachments(self):
		return [d.name for d in get_attachments(self.doctype, self.name)]

	def update_rfq_supplier_status(self, sup_name=None):
		from terminal_framework.query_builder.functions import Count

		SQ = terminal_framework.qb.DocType("Supplier Quotation")
		SQ_Item = terminal_framework.qb.DocType("Supplier Quotation Item")

		for supplier in self.suppliers:
			if sup_name is None or supplier.supplier == sup_name:
				quote_status = _("Received")
				for item in self.items:
					query = (
						terminal_framework.qb.from_(SQ_Item)
						.join(SQ)
						.on(SQ_Item.parent == SQ.name)
						.select(Count(SQ_Item.name).as_("count"))
						.where(SQ.supplier == supplier.supplier)
						.where(SQ_Item.docstatus == 1)
						.where(SQ_Item.request_for_quotation_item == item.name)
					)

					result = query.run(as_dict=True)
					sqi_count = result[0] if result else terminal_framework._dict(count=0)

					if sqi_count.count == 0:
						quote_status = _("Pending")
				supplier.quote_status = quote_status


@terminal_framework.whitelist()
def send_supplier_emails(rfq_name: str):
	check_portal_enabled("Request for Quotation")
	rfq = terminal_framework.get_doc("Request for Quotation", rfq_name)
	if rfq.docstatus == 1:
		rfq.send_to_supplier()


def check_portal_enabled(reference_doctype):
	if not terminal_framework.db.get_value("Portal Menu Item", {"reference_doctype": reference_doctype}, "enabled"):
		terminal_framework.throw(
			_(
				"Access to Request for Quotation from the portal is disabled. To allow access, enable it in Portal Settings."
			)
		)


def get_list_context(context=None):
	from terminal_erp.controllers.website_list_for_contact import get_list_context

	list_context = get_list_context(context)
	list_context.update(
		{
			"show_sidebar": True,
			"show_search": True,
			"no_breadcrumbs": True,
			"title": _("Request for Quotation"),
			"list_template": "templates/includes/list/list.html",
		}
	)
	return list_context


@terminal_framework.whitelist()
def get_pdf(
	name: str,
	supplier: str,
	print_format: str | None = None,
	language: str | None = None,
	letterhead: str | None = None,
):
	doc = terminal_framework.get_doc("Request for Quotation", name)
	if supplier:
		doc.update_supplier_part_no(supplier)

	# permissions get checked in `download_pdf`
	download_pdf(
		doc.doctype,
		doc.name,
		print_format,
		doc=doc,
		language=language,
		letterhead=letterhead or None,
	)


@terminal_framework.whitelist()
def get_supplier_tag():
	filters = {"document_type": "Supplier"}
	tags = list(set(tag.tag for tag in terminal_framework.get_all("Tag Link", filters=filters, fields=["tag"]) if tag))

	return tags


@terminal_framework.whitelist()
@terminal_framework.validate_and_sanitize_search_inputs
def get_rfq_containing_supplier(
	doctype: str | None, txt: str, searchfield: str | None, start: int, page_len: int, filters: dict
):
	rfq = terminal_framework.qb.DocType("Request for Quotation")
	rfq_supplier = terminal_framework.qb.DocType("Request for Quotation Supplier")

	query = (
		terminal_framework.qb.from_(rfq)
		.from_(rfq_supplier)
		.select(rfq.name)
		.distinct()
		.select(rfq.transaction_date, rfq.company)
		.where(
			(rfq.name == rfq_supplier.parent)
			& (rfq_supplier.supplier == filters.get("supplier"))
			& (rfq.docstatus == 1)
			& (rfq.company == filters.get("company"))
		)
		.orderby(rfq.transaction_date, order=Order.asc)
		.limit(page_len)
		.offset(start)
	)

	if txt:
		query = query.where(rfq.name.like(f"%%{txt}%%"))

	if filters.get("transaction_date"):
		query = query.where(rfq.transaction_date == filters.get("transaction_date"))

	rfq_data = query.run(as_dict=1)

	return rfq_data
