import terminal_framework


def execute():
	terminal_framework.reload_doc("setup", "doctype", "currency_exchange")
	terminal_framework.db.sql("""update `tabCurrency Exchange` set for_buying = 1, for_selling = 1""")
