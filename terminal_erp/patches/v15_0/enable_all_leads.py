import terminal_framework


def execute():
	lead = terminal_framework.qb.DocType("Lead")
	terminal_framework.qb.update(lead).set(lead.disabled, 0).set(lead.docstatus, 0).where(
		lead.disabled == 1 and lead.docstatus == 1
	).run()
