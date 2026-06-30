# Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.setup.doctype.employee.test_employee import make_employee
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestEmployeeGroup(Terminal ERPTestSuite):
	pass


def make_employee_group():
	employee = make_employee("testemployee@example.com")
	employee_group = terminal_framework.get_doc(
		{
			"doctype": "Employee Group",
			"employee_group_name": "_Test Employee Group",
			"employee_list": [{"employee": employee}],
		}
	)
	employee_group_exist = terminal_framework.db.exists("Employee Group", "_Test Employee Group")
	if not employee_group_exist:
		employee_group.insert()
		return employee_group.employee_group_name
	else:
		return employee_group_exist


def get_employee_group():
	employee_group = terminal_framework.db.exists("Employee Group", "_Test Employee Group")
	return employee_group
