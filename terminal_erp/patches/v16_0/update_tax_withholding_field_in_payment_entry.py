import terminal_framework
from terminal_framework.query_builder import DocType


def execute():
	if not terminal_framework.db.has_column("Payment Entry", "apply_tax_withholding_amount"):
		return

	pe = DocType("Payment Entry")
	(terminal_framework.qb.update(pe).set(pe.apply_tds, pe.apply_tax_withholding_amount)).run()
