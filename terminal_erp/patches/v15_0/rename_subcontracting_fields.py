import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	if terminal_framework.db.table_exists("Purchase Order Item") and terminal_framework.db.has_column(
		"Purchase Order Item", "sco_qty"
	):
		rename_field("Purchase Order Item", "sco_qty", "subcontracted_quantity")

	if terminal_framework.db.table_exists("Subcontracting Order Item") and terminal_framework.db.has_column(
		"Subcontracting Order Item", "sc_conversion_factor"
	):
		rename_field("Subcontracting Order Item", "sc_conversion_factor", "subcontracting_conversion_factor")
