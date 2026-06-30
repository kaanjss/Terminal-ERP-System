import terminal_framework
from terminal_framework.query_builder import DocType


def execute():
	qlr = DocType("Quotation Lost Reason Detail")
	quotation = DocType("Quotation")

	sub_query = terminal_framework.qb.from_(quotation).select(quotation.name)
	query = terminal_framework.qb.from_(qlr).delete().where(qlr.parent.notin(sub_query))
	query.run()
