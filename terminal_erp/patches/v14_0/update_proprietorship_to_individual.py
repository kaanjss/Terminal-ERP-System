import terminal_framework


def execute():
	for doctype in ["Customer", "Supplier"]:
		field = doctype.lower() + "_type"
		terminal_framework.db.set_value(doctype, {field: "Proprietorship"}, field, "Individual")
