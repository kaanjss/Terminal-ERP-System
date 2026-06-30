import terminal_framework


def execute():
	user_permissions = terminal_framework.db.sql(
		"""select name, for_value from `tabUser Permission`
        where allow='Department'""",
		as_dict=1,
	)
	for d in user_permissions:
		user_permission = terminal_framework.get_doc("User Permission", d.name)
		for new_dept in terminal_framework.db.sql(
			"""select name from tabDepartment
            where ifnull(company, '') != '' and department_name=%s""",
			d.for_value,
		):
			try:
				new_user_permission = terminal_framework.copy_doc(user_permission)
				new_user_permission.for_value = new_dept[0]
				new_user_permission.save()
			except terminal_framework.DuplicateEntryError:
				pass

	terminal_framework.reload_doc("hr", "doctype", "department")
	terminal_framework.db.sql("update tabDepartment set disabled=1 where ifnull(company, '') = ''")
