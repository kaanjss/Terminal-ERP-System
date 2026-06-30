import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	if terminal_framework.db.has_column("Material Request", "price_list"):
		rename_field(
			"Material Request",
			"price_list",
			"buying_price_list",
		)
