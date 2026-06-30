# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestDepartment(Terminal ERPTestSuite):
	def test_remove_department_data(self):
		doc = create_department("Test Department", company="_Test Company")
		terminal_framework.delete_doc("Department", doc.name)


def create_department(department_name, parent_department=None, company=None):
	doc = terminal_framework.get_doc(
		{
			"doctype": "Department",
			"is_group": 0,
			"parent_department": parent_department,
			"department_name": department_name,
			"company": terminal_framework.defaults.get_defaults().company or company,
		}
	).insert()

	return doc
