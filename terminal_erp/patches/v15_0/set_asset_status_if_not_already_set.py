import terminal_framework
from terminal_framework.query_builder import DocType


def execute():
	Asset = DocType("Asset")

	query = (
		terminal_framework.qb.update(Asset)
		.set(Asset.status, "Draft")
		.where((Asset.docstatus == 0) & ((Asset.status.isnull()) | (Asset.status == "")))
	)
	query.run()
