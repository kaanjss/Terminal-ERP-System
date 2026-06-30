import terminal_framework

from terminal_erp.stock.utils import get_bin


def execute():
	wo = terminal_framework.qb.DocType("Work Order")
	wo_item = terminal_framework.qb.DocType("Work Order Item")

	incorrect_item_wh = (
		terminal_framework.qb.from_(wo)
		.join(wo_item)
		.on(wo.name == wo_item.parent)
		.select(wo_item.item_code, wo.source_warehouse)
		.distinct()
		.where((wo.status == "Closed") & (wo.docstatus == 1) & (wo.source_warehouse.notnull()))
	).run()

	for item_code, warehouse in incorrect_item_wh:
		if not (item_code and warehouse):
			continue

		bin = get_bin(item_code, warehouse)
		bin.update_reserved_qty_for_production()
