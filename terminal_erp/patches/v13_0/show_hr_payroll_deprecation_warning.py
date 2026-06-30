import click
import terminal_framework


def execute():
	if "hrms" in terminal_framework.get_installed_apps():
		return

	click.secho(
		"HR and Payroll modules have been moved to a separate app"
		" and will be removed from Terminal ERP in Version 14."
		" Please install the HRMS app when upgrading to Version 14"
		" to continue using the HR and Payroll modules:\n"
		"https://github.com/terminal_framework/hrms",
		fg="yellow",
	)
