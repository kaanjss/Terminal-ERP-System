import terminal_framework

from terminal_erp.setup.setup_wizard.operations.install_fixtures import add_market_segments


def execute():
	terminal_framework.reload_doc("crm", "doctype", "market_segment")

	terminal_framework.local.lang = terminal_framework.db.get_default("lang") or "en"

	add_market_segments()
