# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestCostCenter(Terminal ERPTestSuite):
	def test_cost_center_creation_against_child_node(self):
		cost_center = terminal_framework.get_doc(
			{
				"doctype": "Cost Center",
				"cost_center_name": "_Test Cost Center 3",
				"parent_cost_center": "_Test Cost Center 2 - _TC",
				"is_group": 0,
				"company": "_Test Company",
			}
		)

		self.assertRaises(terminal_framework.ValidationError, cost_center.save)


def create_cost_center(**args):
	args = terminal_framework._dict(args)
	if args.cost_center_name:
		company = args.company or "_Test Company"
		company_abbr = terminal_framework.db.get_value("Company", company, "abbr")
		cc_name = args.cost_center_name + " - " + company_abbr
		if not terminal_framework.db.exists("Cost Center", cc_name):
			cc = terminal_framework.new_doc("Cost Center")
			cc.company = args.company or "_Test Company"
			cc.cost_center_name = args.cost_center_name
			cc.is_group = args.is_group or 0
			cc.parent_cost_center = args.parent_cost_center or "_Test Company - _TC"
			cc.insert()
