# Copyright (c) 2023, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import terminal_framework
from pypika.terms import ExistsCriterion


def execute():
	pl = terminal_framework.qb.DocType("Pick List")
	se = terminal_framework.qb.DocType("Stock Entry")
	dn = terminal_framework.qb.DocType("Delivery Note")

	(
		terminal_framework.qb.update(pl).set(
			pl.status,
			(
				terminal_framework.qb.terms.Case()
				.when(pl.docstatus == 0, "Draft")
				.when(pl.docstatus == 2, "Cancelled")
				.else_("Completed")
			),
		)
	).run()

	(
		terminal_framework.qb.update(pl)
		.set(pl.status, "Open")
		.where(
			(
				ExistsCriterion(
					terminal_framework.qb.from_(se).select(se.name).where((se.docstatus == 1) & (se.pick_list == pl.name))
				)
				| ExistsCriterion(
					terminal_framework.qb.from_(dn).select(dn.name).where((dn.docstatus == 1) & (dn.pick_list == pl.name))
				)
			).negate()
			& (pl.docstatus == 1)
		)
	).run()
