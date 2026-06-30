import terminal_framework
from terminal_framework.query_builder import DocType


def execute():
	POSInvoice = DocType("POS Invoice")

	terminal_framework.qb.update(POSInvoice).set(POSInvoice.status, "Cancelled").where(POSInvoice.docstatus == 2).run()
