import terminal_framework

from terminal_erp.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_doctypes_with_dimensions,
)


def execute():
	accounting_dimensions = terminal_framework.db.sql(
		"""select fieldname from
		`tabAccounting Dimension`""",
		as_dict=1,
	)

	doclist = get_doctypes_with_dimensions()

	for dimension in accounting_dimensions:
		terminal_framework.db.sql(
			"""
			UPDATE `tabCustom Field`
			SET owner = 'Administrator'
			WHERE fieldname = {}
			AND dt IN ({})""".format("%s", ", ".join(["%s"] * len(doclist))),  # nosec
			tuple([dimension.fieldname, *doclist]),
		)
