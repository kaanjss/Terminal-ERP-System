import os

import terminal_framework
from terminal_framework import _


def execute():
	terminal_framework.reload_doc("email", "doctype", "email_template")
	terminal_framework.reload_doc("stock", "doctype", "delivery_settings")

	if not terminal_framework.db.exists("Email Template", _("Dispatch Notification")):
		base_path = terminal_framework.get_app_path("terminal_erp", "stock", "doctype")
		response = terminal_framework.read_file(
			os.path.join(base_path, "delivery_trip/dispatch_notification_template.html")
		)

		terminal_framework.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Dispatch Notification"),
				"response": response,
				"subject": _("Your order is out for delivery!"),
				"owner": terminal_framework.session.user,
			}
		).insert(ignore_permissions=True)

	delivery_settings = terminal_framework.get_doc("Delivery Settings")
	delivery_settings.dispatch_template = _("Dispatch Notification")
	delivery_settings.flags.ignore_links = True
	delivery_settings.save()
