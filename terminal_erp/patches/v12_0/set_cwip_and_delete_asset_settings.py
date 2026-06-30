import terminal_framework
from terminal_framework.utils import cint


def execute():
	"""Get 'Disable CWIP Accounting value' from Asset Settings, set it in 'Enable Capital Work in Progress Accounting' field
	in Company, delete Asset Settings"""

	if terminal_framework.db.exists("DocType", "Asset Settings"):
		terminal_framework.reload_doctype("Asset Category")
		cwip_value = terminal_framework.db.get_single_value("Asset Settings", "disable_cwip_accounting")

		terminal_framework.db.sql("""UPDATE `tabAsset Category` SET enable_cwip_accounting = %s""", cint(cwip_value))

		terminal_framework.db.sql("""DELETE FROM `tabSingles` where doctype = 'Asset Settings'""")
		terminal_framework.delete_doc_if_exists("DocType", "Asset Settings")
