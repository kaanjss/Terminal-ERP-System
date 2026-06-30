import terminal_framework
from terminal_framework.utils import cint


def execute():
	terminal_framework.db.set_single_value(
		"Stock Settings",
		"update_price_list_based_on",
		(
			"Price List Rate"
			if cint(terminal_framework.db.get_single_value("Selling Settings", "editable_price_list_rate"))
			else "Rate"
		),
	)
