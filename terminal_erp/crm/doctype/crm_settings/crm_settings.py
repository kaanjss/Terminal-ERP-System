# Copyright (c) 2021, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework
from terminal_framework import _
from terminal_framework.custom.doctype.custom_field.custom_field import create_custom_fields
from terminal_framework.model.document import Document


class CRMSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.crm.doctype.terminal_framework_crm_allowed_user.terminal_framework_crm_allowed_user import Terminal FrameworkCRMAllowedUser

		allow_lead_duplication_based_on_emails: DF.Check
		allowed_users: DF.TableMultiSelect[Terminal FrameworkCRMAllowedUser]
		auto_creation_of_contact: DF.Check
		campaign_naming_by: DF.Literal["Campaign Name", "Naming Series"]
		carry_forward_communication_and_comments: DF.Check
		close_opportunity_after_days: DF.Int
		default_valid_till: DF.Data | None
		enable_terminal_framework_crm_data_synchronization: DF.Check
		enable_opportunity_creation_from_contact_us: DF.Check
		update_timestamp_on_new_communication: DF.Check
	# end: auto-generated types

	def validate(self):
		terminal_framework.db.set_default("campaign_naming_by", self.get("campaign_naming_by", ""))
		self.validate_enable_opportunity_creation_from_contact_us()
		self.validate_allowed_users()

	def validate_enable_opportunity_creation_from_contact_us(self):
		contact_disabled = terminal_framework.get_single_value("Contact Us Settings", "is_disabled")

		if self.enable_opportunity_creation_from_contact_us and contact_disabled:
			terminal_framework.throw(
				_(
					"Cannot enable Opportunity creation from Contact Us because the Contact Us form is disabled."
				)
			)

	def validate_allowed_users(self):
		if self.enable_terminal_framework_crm_data_synchronization and not self.allowed_users:
			terminal_framework.throw(
				_(
					"Please add at least one user on Allowed Users to allow Data Synchronization from Terminal Framework CRM site."
				)
			)

	def before_save(self):
		self.clear_allowed_users()

	def on_update(self):
		self.custom_fields_for_terminal_framework_crm_data_sync()

	def clear_allowed_users(self):
		if not self.enable_terminal_framework_crm_data_synchronization:
			self.allowed_users = []

	def custom_fields_for_terminal_framework_crm_data_sync(self):
		custom_fields = {
			"Quotation": [
				{
					"fieldname": "crm_deal",
					"fieldtype": "Data",
					"label": "Terminal Framework CRM Deal",
					"insert_after": "party_name",
				}
			],
			"Customer": [
				{
					"fieldname": "crm_deal",
					"fieldtype": "Data",
					"label": "Terminal Framework CRM Deal",
					"insert_after": "prospect_name",
				}
			],
		}

		create_custom_fields(custom_fields, ignore_validate=True)
