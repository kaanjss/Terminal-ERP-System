import terminal_framework


def execute():
	pr_table = terminal_framework.qb.DocType("Pricing Rule")
	(
		terminal_framework.qb.update(pr_table)
		.set(pr_table.has_priority, 1)
		.where((pr_table.priority.isnotnull()) & (pr_table.priority != ""))
	).run()
