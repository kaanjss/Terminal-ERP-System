# Copyright (c) 2020, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import terminal_framework
from terminal_framework import _
from terminal_framework.contacts.doctype.contact.contact import get_default_contact
from terminal_framework.model.document import Document
from terminal_framework.utils import flt, get_time

from terminal_erp.accounts.party import get_party_shipping_address


class Shipment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.stock.doctype.shipment_delivery_note.shipment_delivery_note import ShipmentDeliveryNote
		from terminal_erp.stock.doctype.shipment_parcel.shipment_parcel import ShipmentParcel

		amended_from: DF.Link | None
		awb_number: DF.Data | None
		carrier: DF.Data | None
		carrier_service: DF.Data | None
		delivery_address: DF.TextEditor | None
		delivery_address_name: DF.Link
		delivery_company: DF.Link | None
		delivery_contact: DF.TextEditor | None
		delivery_contact_email: DF.Data | None
		delivery_contact_name: DF.Link | None
		delivery_customer: DF.Link | None
		delivery_supplier: DF.Link | None
		delivery_to: DF.Data | None
		delivery_to_type: DF.Literal["Company", "Customer", "Supplier"]
		description_of_content: DF.SmallText
		incoterm: DF.Link | None
		pallets: DF.Literal["No", "Yes"]
		parcel_template: DF.Link | None
		pickup: DF.Data | None
		pickup_address: DF.TextEditor | None
		pickup_address_name: DF.Link
		pickup_company: DF.Link | None
		pickup_contact: DF.TextEditor | None
		pickup_contact_email: DF.Data | None
		pickup_contact_name: DF.Link | None
		pickup_contact_person: DF.Link | None
		pickup_customer: DF.Link | None
		pickup_date: DF.Date
		pickup_from: DF.Time
		pickup_from_type: DF.Literal["Company", "Customer", "Supplier"]
		pickup_supplier: DF.Link | None
		pickup_to: DF.Time
		pickup_type: DF.Literal["Pickup", "Self delivery"]
		service_provider: DF.Data | None
		shipment_amount: DF.Currency
		shipment_delivery_note: DF.Table[ShipmentDeliveryNote]
		shipment_id: DF.Data | None
		shipment_parcel: DF.Table[ShipmentParcel]
		shipment_type: DF.Literal["Goods", "Documents"]
		status: DF.Literal["Draft", "Submitted", "Booked", "Cancelled", "Completed"]
		total_weight: DF.Float
		tracking_status: DF.Literal["", "In Progress", "Delivered", "Returned", "Lost"]
		tracking_status_info: DF.Data | None
		tracking_url: DF.SmallText | None
		value_of_goods: DF.Currency
	# end: auto-generated types

	def on_discard(self):
		self.db_set("status", "Cancelled")

	def validate(self):
		self.validate_weight()
		self.validate_pickup_time()
		self.set_value_of_goods()
		self.set_total_weight()
		if self.docstatus == 0:
			self.status = "Draft"

	def on_submit(self):
		if not self.shipment_parcel:
			terminal_framework.throw(_("Please enter Shipment Parcel information"))
		if self.value_of_goods == 0:
			terminal_framework.throw(_("Value of goods cannot be 0"))
		self.db_set("status", "Submitted")

	def on_cancel(self):
		self.db_set("status", "Cancelled")

	def validate_weight(self):
		for parcel in self.shipment_parcel:
			if flt(parcel.weight) <= 0:
				terminal_framework.throw(_("Parcel weight cannot be 0"))

	def set_total_weight(self):
		self.total_weight = self.get_total_weight()

	def get_total_weight(self):
		return sum(flt(parcel.weight) * parcel.count for parcel in self.shipment_parcel if parcel.count > 0)

	def validate_pickup_time(self):
		if self.pickup_from and self.pickup_to and get_time(self.pickup_to) < get_time(self.pickup_from):
			terminal_framework.throw(_("Pickup To time should be greater than Pickup From time"))

	def set_value_of_goods(self):
		value_of_goods = 0
		for entry in self.get("shipment_delivery_note"):
			value_of_goods += flt(entry.get("grand_total"))
		self.value_of_goods = value_of_goods if value_of_goods else self.value_of_goods


@terminal_framework.whitelist()
def get_address_name(ref_doctype: str, docname: str):
	# Return address name
	return get_party_shipping_address(ref_doctype, docname)


@terminal_framework.whitelist()
def get_contact_name(ref_doctype: str, docname: str):
	# Return address name
	return get_default_contact(ref_doctype, docname)


@terminal_framework.whitelist()
def get_company_contact(user: str):
	terminal_framework.has_permission("User", "read", throw=True)

	contact = terminal_framework.db.get_value(
		"User",
		user,
		[
			"first_name",
			"last_name",
			"email",
			"phone",
			"mobile_no",
			"gender",
		],
		as_dict=1,
	)
	if not contact.phone:
		contact.phone = contact.mobile_no
	return contact
