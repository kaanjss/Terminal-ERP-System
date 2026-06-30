import click
import terminal_framework


def execute():
	if (
		not terminal_framework.db.exists("Company", {"country": "India"})
		or "india_compliance" in terminal_framework.get_installed_apps()
	):
		return

	click.secho(
		"India-specific regional features have been moved to a separate app"
		" and will be removed from Terminal ERP in Version 14."
		" Please install India Compliance after upgrading to Version 14:\n"
		"https://github.com/resilient-tech/india-compliance",
		fg="yellow",
	)
