import terminal_framework

# Set department value based on employee value


def execute():
	doctypes_to_update = {
		"projects": ["Activity Cost", "Timesheet"],
		"setup": ["Sales Person"],
	}

	for module, doctypes in doctypes_to_update.items():
		for doctype in doctypes:
			if terminal_framework.db.table_exists(doctype):
				terminal_framework.reload_doc(module, "doctype", terminal_framework.scrub(doctype))
				terminal_framework.db.sql(
					"""
					update `tab%s` dt
					set department=(select department from `tabEmployee` where name=dt.employee)
				"""
					% doctype
				)
