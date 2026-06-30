# Copyright (c) 2021, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.stock.doctype.repost_item_valuation.repost_item_valuation import get_recipients
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestStockRepostingSettings(Terminal ERPTestSuite):
	def test_notify_reposting_error_to_role(self):
		role = "Notify Reposting Role"

		if not terminal_framework.db.exists("Role", role):
			terminal_framework.get_doc({"doctype": "Role", "role_name": role}).insert(ignore_permissions=True)

		user = "notify_reposting_error@test.com"
		if not terminal_framework.db.exists("User", user):
			terminal_framework.get_doc(
				{
					"doctype": "User",
					"email": user,
					"first_name": "Test",
					"language": "en",
					"time_zone": "Asia/Kolkata",
					"send_welcome_email": 0,
					"roles": [{"role": role}],
				}
			).insert(ignore_permissions=True)

		terminal_framework.db.set_single_value("Stock Reposting Settings", "notify_reposting_error_to_role", "")

		users = get_recipients()
		self.assertNotIn(user, users)

		terminal_framework.db.set_single_value("Stock Reposting Settings", "notify_reposting_error_to_role", role)

		users = get_recipients()
		self.assertIn(user, users)
