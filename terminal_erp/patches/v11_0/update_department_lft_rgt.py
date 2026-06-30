import terminal_framework
from terminal_framework import _
from terminal_framework.utils.nestedset import rebuild_tree


def execute():
	"""assign lft and rgt appropriately"""
	terminal_framework.reload_doc("setup", "doctype", "department")
	if not terminal_framework.db.exists("Department", _("All Departments")):
		terminal_framework.get_doc(
			{"doctype": "Department", "department_name": _("All Departments"), "is_group": 1}
		).insert(ignore_permissions=True, ignore_mandatory=True)

	terminal_framework.db.sql(
		"""update `tabDepartment` set parent_department = '{}'
		where is_group = 0""".format(_("All Departments"))
	)

	rebuild_tree("Department")
