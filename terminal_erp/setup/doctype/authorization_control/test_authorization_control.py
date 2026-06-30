# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestAuthorizationControl(Terminal ERPTestSuite):
	def test_validate_approving_authority_raises_when_over_limit(self):
		# Exercises validate_approving_authority -> the based_on query-builder lookups and the
		# coalesce()-based rule lookups (formerly ifnull, which is invalid on Postgres).
		if not terminal_framework.db.exists("Role", "_Test Approver Role"):
			terminal_framework.get_doc({"doctype": "Role", "role_name": "_Test Approver Role"}).insert()

		# Run as a non-admin user without the approving role; Administrator implicitly holds every
		# role, so the not-authorized branch would never fire as Administrator.
		user = "_test_auth_control_user@example.com"
		if not terminal_framework.db.exists("User", user):
			terminal_framework.get_doc(
				{
					"doctype": "User",
					"email": user,
					"first_name": "Auth Control",
					"send_welcome_email": 0,
					"roles": [{"role": "Sales User"}],
				}
			).insert(ignore_permissions=True)

		rule = terminal_framework.get_doc(
			{
				"doctype": "Authorization Rule",
				"transaction": "Sales Order",
				"based_on": "Grand Total",
				"company": "_Test Company",
				"value": 1000,
				"approving_role": "_Test Approver Role",
			}
		).insert()
		self.addCleanup(terminal_framework.delete_doc, "Authorization Rule", rule.name, force=1)

		controller = terminal_framework.get_cached_doc("Authorization Control")
		terminal_framework.set_user(user)
		self.addCleanup(terminal_framework.set_user, "Administrator")
		# User lacks _Test Approver Role and the total exceeds the rule value -> not authorized.
		self.assertRaises(
			terminal_framework.ValidationError,
			controller.validate_approving_authority,
			"Sales Order",
			"_Test Company",
			5000,
		)

	def test_get_value_based_rule_runs(self):
		# Exercises the four query-builder lookups (incl. the Employee designation subquery) added in
		# get_value_based_rule; with no matching rule they must run and return empty on both engines.
		controller = terminal_framework.get_cached_doc("Authorization Control")
		result = controller.get_value_based_rule("Expense Claim", "_NONEXISTENT-EMP", 100, "_Test Company")
		self.assertEqual(list(result), [])
