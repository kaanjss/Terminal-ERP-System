import terminal_framework
from terminal_framework.utils.nestedset import rebuild_tree


def execute():
	terminal_framework.reload_doc("setup", "doctype", "company")
	rebuild_tree("Company")
