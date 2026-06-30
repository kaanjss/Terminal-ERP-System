import terminal_framework
from terminal_framework.query_builder import DocType
from terminal_framework.query_builder.functions import Sum


def execute():
	PurchaseOrderItem = DocType("Purchase Order Item")
	MaterialRequestItem = DocType("Material Request Item")

	poi_query = (
		terminal_framework.qb.from_(PurchaseOrderItem)
		.select(PurchaseOrderItem.sales_order_item, Sum(PurchaseOrderItem.stock_qty))
		.where(PurchaseOrderItem.sales_order_item.isnotnull() & PurchaseOrderItem.docstatus == 1)
		.groupby(PurchaseOrderItem.sales_order_item)
	)

	mri_query = (
		terminal_framework.qb.from_(MaterialRequestItem)
		.select(MaterialRequestItem.sales_order_item, Sum(MaterialRequestItem.stock_qty))
		.where(MaterialRequestItem.sales_order_item.isnotnull() & MaterialRequestItem.docstatus == 1)
		.groupby(MaterialRequestItem.sales_order_item)
	)

	poi_data = poi_query.run()
	mri_data = mri_query.run()

	updates_against_poi = {data[0]: {"ordered_qty": data[1]} for data in poi_data}
	updates_against_mri = {data[0]: {"requested_qty": data[1], "ordered_qty": 0} for data in mri_data}

	terminal_framework.db.auto_commit_on_many_writes = 1
	terminal_framework.db.bulk_update("Sales Order Item", updates_against_mri)
	terminal_framework.db.bulk_update("Sales Order Item", updates_against_poi)
	terminal_framework.db.auto_commit_on_many_writes = 0
