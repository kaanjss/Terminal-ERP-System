import terminal_framework
from terminal_framework.utils import flt


def execute():
	budgets = terminal_framework.get_all("Budget", filters={"docstatus": ["in", [0, 1]]}, fields=["name"])

	for b in budgets:
		doc = terminal_framework.get_doc("Budget", b.name)
		total = sum(flt(row.amount) for row in doc.budget_distribution)
		doc.db_set("budget_distribution_total", total, update_modified=False)
