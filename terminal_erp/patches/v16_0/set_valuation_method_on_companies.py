import terminal_framework


def execute():
	valuation_method = terminal_framework.get_single_value("Stock Settings", "valuation_method")
	for company in terminal_framework.get_all("Company", pluck="name"):
		terminal_framework.db.set_value("Company", company, "valuation_method", valuation_method)
