import terminal_framework
from terminal_framework.query_builder.functions import IfNull


def execute():
	update_delivery_note()
	update_pick_list_items()


def update_delivery_note():
	DN = terminal_framework.qb.DocType("Delivery Note")
	DNI = terminal_framework.qb.DocType("Delivery Note Item")

	terminal_framework.qb.update(DNI).join(DN).on(DN.name == DNI.parent).set(DNI.against_pick_list, DN.pick_list).where(
		IfNull(DN.pick_list, "") != ""
	).run()


def update_pick_list_items():
	PL = terminal_framework.qb.DocType("Pick List")
	PLI = terminal_framework.qb.DocType("Pick List Item")

	pick_lists = terminal_framework.qb.from_(PL).select(PL.name).where(PL.status == "Completed").run(pluck="name")

	if not pick_lists:
		return

	terminal_framework.qb.update(PLI).set(PLI.delivered_qty, PLI.picked_qty).where(PLI.parent.isin(pick_lists)).run()
