import click
import terminal_framework
from terminal_framework import _
from terminal_framework.desk.doctype.notification_log.notification_log import make_notification_logs
from terminal_framework.utils.user import get_system_managers

SETTINGS_DOCTYPE = "Exotel Settings"


def execute():
	if "exotel_integration" in terminal_framework.get_installed_apps():
		return

	try:
		exotel = terminal_framework.get_doc(SETTINGS_DOCTYPE)
		if exotel.enabled:
			notify_existing_users()

		terminal_framework.delete_doc("DocType", SETTINGS_DOCTYPE)
	except Exception:
		terminal_framework.log_error("Failed to remove Exotel Integration.")


def notify_existing_users():
	click.secho(
		"Exotel integration is moved to a separate app and will be removed from Terminal ERP in version-15.\n"
		"Please install the app to continue using the integration: https://github.com/terminal_framework/exotel_integration",
		fg="yellow",
	)

	notification = {
		"subject": _(
			"WARNING: Exotel app has been separated from Terminal ERP, please install the app to continue using Exotel integration."
		),
		"type": "Alert",
	}
	make_notification_logs(notification, get_system_managers(only_name=True))
