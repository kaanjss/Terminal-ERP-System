import terminal_framework


def execute():
	terminal_framework.reload_doctype("Maintenance Visit")
	terminal_framework.reload_doctype("Maintenance Visit Purpose")

	# Updates the Maintenance Schedule link to fetch serial nos
	from terminal_framework.query_builder.functions import Coalesce

	mvp = terminal_framework.qb.DocType("Maintenance Visit Purpose")
	mv = terminal_framework.qb.DocType("Maintenance Visit")

	terminal_framework.qb.update(mv).join(mvp).on(mvp.parent == mv.name).set(
		mv.maintenance_schedule, Coalesce(mvp.prevdoc_docname, "")
	).where((mv.maintenance_type == "Scheduled") & (mvp.prevdoc_docname.notnull()) & (mv.docstatus < 2)).run(
		as_dict=1
	)
