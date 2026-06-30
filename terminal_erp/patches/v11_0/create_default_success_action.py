import terminal_framework

from terminal_erp.setup.install import create_default_success_action


def execute():
	terminal_framework.reload_doc("core", "doctype", "success_action")
	create_default_success_action()
