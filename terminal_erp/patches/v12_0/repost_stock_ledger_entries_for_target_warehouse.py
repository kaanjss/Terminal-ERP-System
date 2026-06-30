# Copyright (c) 2020, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	warehouse_perm = terminal_framework.get_all(
		"User Permission",
		fields=[{"COUNT": "*", "as": "p_count"}, "is_default", "user"],
		filters={"allow": "Warehouse"},
		group_by="user",
	)

	if not warehouse_perm:
		return

	execute_patch = False
	for perm_data in warehouse_perm:
		if perm_data.p_count == 1 or (
			perm_data.p_count > 1
			and terminal_framework.get_all(
				"User Permission",
				filters={"user": perm_data.user, "allow": "warehouse", "is_default": 1},
				limit=1,
			)
		):
			execute_patch = True
			break

	if not execute_patch:
		return

	for doctype in ["Sales Invoice", "Delivery Note"]:
		if not terminal_framework.get_meta(doctype + " Item").get_field("target_warehouse").hidden:
			continue

		cond = ""
		if doctype == "Sales Invoice":
			cond = " AND parent_doc.update_stock = 1"

		data = terminal_framework.db.sql(
			f""" SELECT parent_doc.name as name, child_doc.name as child_name
			FROM
				`tab{doctype}` parent_doc, `tab{doctype} Item` child_doc
			WHERE
				parent_doc.name = child_doc.parent AND parent_doc.docstatus < 2
				AND child_doc.target_warehouse is not null AND child_doc.target_warehouse != ''
				AND child_doc.creation > '2020-04-16' {cond}
		""",
			as_dict=1,
		)

		if data:
			names = [d.child_name for d in data]
			terminal_framework.db.sql(
				""" UPDATE `tab{} Item` set target_warehouse = null
				WHERE name in ({}) """.format(doctype, ",".join(["%s"] * len(names))),
				tuple(names),
			)

			terminal_framework.db.sql(
				""" UPDATE `tabPacked Item` set target_warehouse = null
				WHERE parenttype = '{}' and parent_detail_docname in ({})
			""".format(doctype, ",".join(["%s"] * len(names))),
				tuple(names),
			)

			parent_names = list(set([d.name for d in data]))

			for d in parent_names:
				doc = terminal_framework.get_doc(doctype, d)
				if doc.docstatus != 1:
					continue

				doc.docstatus = 2
				doc.update_stock_ledger()
				doc.make_gl_entries_on_cancel(repost_future_gle=False)

				# update stock & gl entries for submit state of PR
				doc.docstatus = 1
				doc.update_stock_ledger()
				doc.make_gl_entries()

	if terminal_framework.get_meta("Sales Order Item").get_field("target_warehouse").hidden:
		terminal_framework.db.sql(
			""" UPDATE `tabSales Order Item` set target_warehouse = null
			WHERE creation > '2020-04-16' and docstatus < 2 """
		)

		terminal_framework.db.sql(
			""" UPDATE `tabPacked Item` set target_warehouse = null
			WHERE creation > '2020-04-16' and docstatus < 2 and parenttype = 'Sales Order' """
		)
