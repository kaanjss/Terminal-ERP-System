import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	if terminal_framework.db.has_column("Delivery Stop", "lock"):
		rename_field("Delivery Stop", "lock", "locked")
