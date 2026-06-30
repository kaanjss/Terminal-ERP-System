import click
import terminal_framework


def execute():
	if "ksa" in terminal_framework.get_installed_apps():
		return

	doctypes = ["KSA VAT Setting", "KSA VAT Purchase Account", "KSA VAT Sales Account"]
	for doctype in doctypes:
		terminal_framework.delete_doc("DocType", doctype, ignore_missing=True)

	print_formats = ["KSA POS Invoice", "KSA VAT Invoice"]
	for print_format in print_formats:
		terminal_framework.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	reports = ["KSA VAT"]
	for report in reports:
		terminal_framework.delete_doc("Report", report, ignore_missing=True, force=True)

	click.secho(
		"Region Saudi Arabia(KSA) is moved to a separate app"
		"Please install the app to continue using the module: https://github.com/8848digital/KSA",
		fg="yellow",
	)
