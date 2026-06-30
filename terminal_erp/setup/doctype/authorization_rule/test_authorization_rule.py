# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestAuthorizationRule(Terminal ERPTestSuite):
	def test_duplicate_rule_is_blocked(self):
		"""check_duplicate_entry uses terminal_framework.get_all over Authorization Rule; a second rule with the
		same transaction/based_on/approving_role/value must be rejected as a duplicate (the converted
		query must find the existing row on both engines)."""

		def make_rule():
			return terminal_framework.get_doc(
				{
					"doctype": "Authorization Rule",
					"transaction": "Sales Order",
					"based_on": "Grand Total",
					"approving_role": "Sales Manager",
					"value": 100000,
				}
			)

		make_rule().insert(ignore_permissions=True)
		# a second identical rule must be caught by the converted duplicate-check query
		self.assertRaises(terminal_framework.ValidationError, make_rule().insert, ignore_permissions=True)
