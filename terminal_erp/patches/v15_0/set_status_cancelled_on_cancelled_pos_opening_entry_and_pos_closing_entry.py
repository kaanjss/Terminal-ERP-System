import terminal_framework
from terminal_framework.query_builder import DocType


def execute():
	POSOpeningEntry = DocType("POS Opening Entry")
	POSClosingEntry = DocType("POS Closing Entry")

	terminal_framework.qb.update(POSOpeningEntry).set(POSOpeningEntry.status, "Cancelled").where(
		POSOpeningEntry.docstatus == 2
	).run()
	terminal_framework.qb.update(POSClosingEntry).set(POSClosingEntry.status, "Cancelled").where(
		POSClosingEntry.docstatus == 2
	).run()
