import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	if terminal_framework.db.has_column("Purchase Order Item", "subcontracted_quantity"):
		rename_field("Purchase Order Item", "subcontracted_quantity", "subcontracted_qty")
