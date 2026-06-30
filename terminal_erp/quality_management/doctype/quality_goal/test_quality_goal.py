# Copyright (c) 2018, Terminal Framework and Contributors
# See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestQualityGoal(Terminal ERPTestSuite):
	def test_quality_goal(self):
		# no code, just a basic sanity check
		goal = get_quality_goal()
		self.assertTrue(goal)
		goal.delete()


def get_quality_goal():
	return terminal_framework.get_doc(
		doctype="Quality Goal",
		goal="Test Quality Module",
		frequency="Daily",
		objectives=[dict(objective="Check test cases", target="100", uom="Percent")],
	).insert()
