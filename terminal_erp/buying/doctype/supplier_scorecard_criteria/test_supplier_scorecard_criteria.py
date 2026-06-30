# Copyright (c) 2017, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt


import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestSupplierScorecardCriteria(Terminal ERPTestSuite):
	def test_variables_exist(self):
		for d in test_good_criteria:
			terminal_framework.get_doc(d).insert()

		self.assertRaises(terminal_framework.ValidationError, terminal_framework.get_doc(test_bad_criteria[0]).insert)

	def test_formula_validate(self):
		self.assertRaises(terminal_framework.ValidationError, terminal_framework.get_doc(test_bad_criteria[1]).insert)


test_good_criteria = [
	{
		"name": "Delivery",
		"weight": 40.0,
		"doctype": "Supplier Scorecard Criteria",
		"formula": "(({cost_of_on_time_shipments} / {tot_cost_shipments}) if {tot_cost_shipments} > 0 else 1 )* 100",
		"criteria_name": "Delivery",
		"max_score": 100.0,
	},
]

test_bad_criteria = [
	{
		"name": "Fake Criteria 1",
		"weight": 40.0,
		"doctype": "Supplier Scorecard Criteria",
		"formula": "(({fake_variable} / {tot_cost_shipments}) if {tot_cost_shipments} > 0 else 1 )* 100",  # Invalid variable name
		"criteria_name": "Fake Criteria 1",
		"max_score": 100.0,
	},
	{
		"name": "Fake Criteria 2",
		"weight": 40.0,
		"doctype": "Supplier Scorecard Criteria",
		"formula": "(({cost_of_on_time_shipments} {cost_of_on_time_shipments} / {tot_cost_shipments}))* 100",  # Two variables beside eachother
		"criteria_name": "Fake Criteria 2",
		"max_score": 100.0,
	},
]
