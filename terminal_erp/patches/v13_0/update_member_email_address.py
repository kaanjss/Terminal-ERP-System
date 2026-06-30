# Copyright (c) 2020, Terminal Framework Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	"""add value to email_id column from email"""

	if terminal_framework.db.has_column("Member", "email"):
		# Get all members
		for member in terminal_framework.db.get_all("Member", pluck="name"):
			# Check if email_id already exists
			if not terminal_framework.db.get_value("Member", member, "email_id"):
				# fetch email id from the user linked field email
				email = terminal_framework.db.get_value("Member", member, "email")

				# Set the value for it
				terminal_framework.db.set_value("Member", member, "email_id", email)

	if terminal_framework.db.exists("DocType", "Membership Settings"):
		rename_field("Membership Settings", "enable_auto_invoicing", "enable_invoicing")
