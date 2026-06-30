import terminal_framework

from terminal_erp.selling.doctype.sales_order.sales_order import update_produced_qty_in_so_item


def execute():
	terminal_framework.reload_doctype("Sales Order Item")
	terminal_framework.reload_doctype("Sales Order")

	for d in terminal_framework.get_all(
		"Work Order",
		fields=["sales_order", "sales_order_item"],
		filters={"sales_order": ("!=", ""), "sales_order_item": ("!=", "")},
	):
		# update produced qty in sales order
		update_produced_qty_in_so_item(d.sales_order, d.sales_order_item)
