import terminal_framework

from terminal_erp.setup.install import setup_currency_exchange


def execute():
	terminal_framework.reload_doc("accounts", "doctype", "currency_exchange_settings")
	setup_currency_exchange()
