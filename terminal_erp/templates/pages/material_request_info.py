# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework
from terminal_framework import _
from terminal_framework.utils import flt


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = terminal_framework.get_doc(terminal_framework.form_dict.doctype, terminal_framework.form_dict.name)
	if hasattr(context.doc, "set_indicator"):
		context.doc.set_indicator()

	context.parents = terminal_framework.form_dict.parents
	context.title = terminal_framework.form_dict.name

	if not terminal_framework.has_website_permission(context.doc):
		terminal_framework.throw(_("Not Permitted"), terminal_framework.PermissionError)

	default_print_format = terminal_framework.db.get_value(
		"Property Setter",
		dict(property="default_print_format", doc_type=terminal_framework.form_dict.doctype),
		"value",
	)
	if default_print_format:
		context.print_format = default_print_format
	else:
		context.print_format = "Standard"
	context.doc.items = get_more_items_info(context.doc.items, context.doc.name)


def get_more_items_info(items, material_request):
	for item in items:
		item.customer_provided = terminal_framework.get_value("Item", item.item_code, "is_customer_provided_item")
		wo = terminal_framework.qb.DocType("Work Order")
		wo_item = terminal_framework.qb.DocType("Work Order Item")
		item.work_orders = (
			terminal_framework.qb.from_(wo_item)
			.inner_join(wo)
			.on(wo_item.parent == wo.name)
			.select(wo.name, wo.status, wo_item.consumed_qty)
			.where(
				(wo_item.item_code == item.item_code)
				& (wo_item.consumed_qty == 0)
				& (wo.status.notin(["Completed", "Cancelled", "Stopped"]))
			)
			.orderby(wo.name)
			.run(as_dict=1)
		)
		item.delivered_qty = flt(
			terminal_framework.get_all(
				"Stock Entry Detail",
				filters={
					"material_request": material_request,
					"item_code": item.item_code,
					"docstatus": 1,
				},
				fields=[{"SUM": "transfer_qty", "as": "transfer_qty"}],
			)[0].transfer_qty
		)
	return items
