import click
import terminal_framework


def execute():
	if "taxjar_integration" in terminal_framework.get_installed_apps():
		return

	doctypes = ["TaxJar Settings", "TaxJar Nexus", "Product Tax Category"]
	for doctype in doctypes:
		terminal_framework.delete_doc("DocType", doctype, ignore_missing=True)

	click.secho(
		"Taxjar Integration is moved to a separate app"
		"Please install the app to continue using the module: https://github.com/terminal_framework/taxjar_integration",
		fg="yellow",
	)
