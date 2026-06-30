import terminal_framework
from terminal_framework.query_builder import DocType


def execute():
	default_accounting_dimension()
	ADF = DocType("Accounting Dimension Filter")
	AD = DocType("Accounting Dimension")

	accounting_dimension_filter = (
		terminal_framework.qb.from_(ADF)
		.join(AD)
		.on(AD.document_type == ADF.accounting_dimension)
		.select(ADF.name, AD.fieldname, ADF.accounting_dimension)
	).run(as_dict=True)

	for doc in accounting_dimension_filter:
		value = doc.fieldname or terminal_framework.scrub(doc.accounting_dimension)
		terminal_framework.db.set_value(
			"Accounting Dimension Filter",
			doc.name,
			"fieldname",
			value,
			update_modified=False,
		)


def default_accounting_dimension():
	ADF = DocType("Accounting Dimension Filter")
	for dim in ("Cost Center", "Project"):
		(
			terminal_framework.qb.update(ADF)
			.set(ADF.fieldname, terminal_framework.scrub(dim))
			.where(ADF.accounting_dimension == dim)
			.run()
		)
