import click
import terminal_framework


def execute():
	if "lending" in terminal_framework.get_installed_apps():
		return

	click.secho(
		"Loan Management module has been moved to a separate app"
		" and will be removed from Terminal ERP in Version 15."
		" Please install the Lending app when upgrading to Version 15"
		" to continue using the Loan Management module:\n"
		"https://github.com/terminal_framework/lending",
		fg="yellow",
	)
