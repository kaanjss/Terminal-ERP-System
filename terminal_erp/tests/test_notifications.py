# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

import terminal_framework
from terminal_framework.desk import notifications

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestNotifications(Terminal ERPTestSuite):
	def test_get_notifications_for_targets(self):
		"""
		Test notification config entries for targets as percentages
		"""

		company = terminal_framework.get_all("Company")[0]
		terminal_framework.db.set_value("Company", company.name, "monthly_sales_target", 10000)
		terminal_framework.db.set_value("Company", company.name, "total_monthly_sales", 1000)

		config = notifications.get_notification_config()
		doc_target_percents = notifications.get_notifications_for_targets(config, {})

		self.assertEqual(doc_target_percents["Company"][company.name], 10)

		terminal_framework.db.set_value("Company", company.name, "monthly_sales_target", 2000)
		terminal_framework.db.set_value("Company", company.name, "total_monthly_sales", 0)

		config = notifications.get_notification_config()
		doc_target_percents = notifications.get_notifications_for_targets(config, {})

		self.assertEqual(doc_target_percents["Company"][company.name], 0)
