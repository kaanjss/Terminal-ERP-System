import terminal_framework
import terminal_framework.defaults


def execute():
	if terminal_framework.db.has_column("Material Request", "buying_price_list") and (
		default_buying_price_list := terminal_framework.defaults.get_defaults().buying_price_list
	):
		docs = terminal_framework.get_all(
			"Material Request", filters={"buying_price_list": ["is", "not set"], "docstatus": 1}, pluck="name"
		)
		terminal_framework.db.auto_commit_on_many_writes = 1
		try:
			for doc in docs:
				terminal_framework.db.set_value("Material Request", doc, "buying_price_list", default_buying_price_list)
		finally:
			terminal_framework.db.auto_commit_on_many_writes = 0
