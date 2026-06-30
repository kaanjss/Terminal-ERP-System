import terminal_framework
from terminal_framework.custom.doctype.custom_field.custom_field import create_custom_field


def execute():
	terminal_framework.reload_doc("accounts", "doctype", "accounting_dimension")
	accounting_dimensions = terminal_framework.db.sql(
		"""select fieldname, label, document_type, disabled from
		`tabAccounting Dimension`""",
		as_dict=1,
	)

	if not accounting_dimensions:
		return

	count = 1
	for d in accounting_dimensions:
		if count % 2 == 0:
			insert_after_field = "dimension_col_break"
		else:
			insert_after_field = "accounting_dimensions_section"

		for doctype in ["POS Invoice", "POS Invoice Item"]:
			field = terminal_framework.db.get_value("Custom Field", {"dt": doctype, "fieldname": d.fieldname})

			if field:
				continue
			meta = terminal_framework.get_meta(doctype, cached=False)
			fieldnames = [d.fieldname for d in meta.get("fields")]

			df = {
				"fieldname": d.fieldname,
				"label": d.label,
				"fieldtype": "Link",
				"options": d.document_type,
				"insert_after": insert_after_field,
			}

			if df["fieldname"] not in fieldnames:
				create_custom_field(doctype, df)
				terminal_framework.clear_cache(doctype=doctype)

		count += 1
