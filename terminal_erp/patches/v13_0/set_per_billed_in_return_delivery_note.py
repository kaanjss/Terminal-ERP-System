# Copyright (c) 2022, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework


def execute():
	dn = terminal_framework.qb.DocType("Delivery Note")
	dn_item = terminal_framework.qb.DocType("Delivery Note Item")

	dn_list = (
		terminal_framework.qb.from_(dn)
		.inner_join(dn_item)
		.on(dn.name == dn_item.parent)
		.select(dn.name)
		.where(dn.docstatus == 1)
		.where(dn.is_return == 1)
		.where(dn.per_billed < 100)
		.where(dn_item.returned_qty > 0)
		.run(as_dict=True)
	)

	terminal_framework.qb.update(dn_item).inner_join(dn).on(dn.name == dn_item.parent).set(dn_item.returned_qty, 0).where(
		dn.is_return == 1
	).where(dn_item.returned_qty > 0).run()

	for d in dn_list:
		dn_doc = terminal_framework.get_doc("Delivery Note", d.get("name"))
		dn_doc.run_method("update_billing_status")
