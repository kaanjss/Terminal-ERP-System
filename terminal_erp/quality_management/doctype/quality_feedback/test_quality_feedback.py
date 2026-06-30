# Copyright (c) 2019, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestQualityFeedback(Terminal ERPTestSuite):
	def test_quality_feedback(self):
		template = terminal_framework.get_doc(
			doctype="Quality Feedback Template",
			template="Test Template",
			parameters=[dict(parameter="Test Parameter 1"), dict(parameter="Test Parameter 2")],
		).insert()

		feedback = terminal_framework.get_doc(
			doctype="Quality Feedback",
			template=template.name,
			document_type="User",
			document_name=terminal_framework.session.user,
		).insert()

		self.assertEqual(template.parameters[0].parameter, feedback.parameters[0].parameter)

		feedback.delete()
		template.delete()
