import terminal_framework


def execute():
	terminal_framework.reload_doctype("Task")

	# add "Completed" if customized
	property_setter_name = terminal_framework.db.exists(
		"Property Setter", dict(doc_type="Task", field_name="status", property="options")
	)
	if property_setter_name:
		property_setter = terminal_framework.get_doc("Property Setter", property_setter_name)
		if "Completed" not in property_setter.value:
			property_setter.value = property_setter.value + "\nCompleted"
			property_setter.save()

	# renamed default status to Completed as status "Closed" is ambiguous
	terminal_framework.db.sql('update tabTask set status = "Completed" where status = "Closed"')
