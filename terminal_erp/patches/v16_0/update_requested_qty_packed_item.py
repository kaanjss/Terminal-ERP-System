import terminal_framework
from terminal_framework.query_builder.functions import Sum


def execute():
	MaterialRequestItem = terminal_framework.qb.DocType("Material Request Item")

	mri_query = (
		terminal_framework.qb.from_(MaterialRequestItem)
		.select(MaterialRequestItem.packed_item, Sum(MaterialRequestItem.qty))
		.where((MaterialRequestItem.packed_item.isnotnull()) & (MaterialRequestItem.docstatus == 1))
		.groupby(MaterialRequestItem.packed_item)
	)

	mri_data = mri_query.run()

	if not mri_data:
		return

	updates_against_mr = {data[0]: {"requested_qty": data[1]} for data in mri_data}

	terminal_framework.db.auto_commit_on_many_writes = True
	terminal_framework.db.bulk_update("Packed Item", updates_against_mr)
	terminal_framework.db.auto_commit_on_many_writes = False
