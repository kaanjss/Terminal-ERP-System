# Copyright (c) 2019, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestIssuePriority(Terminal ERPTestSuite):
	def test_priorities(self):
		make_priorities()
		priorities = terminal_framework.get_list("Issue Priority")

		for priority in priorities:
			self.assertIn(priority.name, ["Low", "Medium", "High"])


def make_priorities():
	insert_priority("Low")
	insert_priority("Medium")
	insert_priority("High")


def insert_priority(name):
	if not terminal_framework.db.exists("Issue Priority", name):
		terminal_framework.get_doc({"doctype": "Issue Priority", "name": name}).insert(ignore_permissions=True)
