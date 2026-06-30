# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework

from terminal_erp.crm.report.prospects_engaged_but_not_converted.prospects_engaged_but_not_converted import (
	execute,
)
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestProspectsEngagedButNotConverted(Terminal ERPTestSuite):
	def test_lead_with_received_communications_appears(self):
		"""The report lists non-converted Leads that have Communications referencing them
		(reference_doctype="Lead", reference_name=lead.name) with sent_or_received="Received".
		Seed one Lead and two such Received Communications, then assert the Lead surfaces in the
		report data and that the emitted row carries the Lead -> reference_doctype/reference_name
		linkage the get_data() join relies on. Asserting a concrete row (not a count) keeps this a
		real-state smoke test that exercises the same path on both MariaDB and Postgres."""
		lead_name = "_Test Prospect Engaged"
		email = "_test_prospect_engaged@example.com"

		lead = terminal_framework.db.exists("Lead", {"lead_name": lead_name})
		if lead:
			lead = terminal_framework.get_doc("Lead", lead)
		else:
			lead = terminal_framework.get_doc(
				{
					"doctype": "Lead",
					"lead_name": lead_name,
					"email_id": email,
					"company_name": "_Test Prospect Org",
				}
			).insert(ignore_permissions=True)

		# A fresh, non-converted Lead is required for it to pass the report's lead filters.
		self.assertNotEqual(lead.status, "Converted")

		for subject in ("_test prospect engaged 1", "_test prospect engaged 2"):
			if not terminal_framework.db.exists(
				"Communication",
				{
					"reference_doctype": "Lead",
					"reference_name": lead.name,
					"subject": subject,
				},
			):
				terminal_framework.get_doc(
					{
						"doctype": "Communication",
						"communication_type": "Communication",
						"subject": subject,
						"content": subject,
						"sent_or_received": "Received",
						"reference_doctype": "Lead",
						"reference_name": lead.name,
					}
				).insert(ignore_permissions=True)

		# filters are accessed via .get(...) in the report, so a plain _dict suffices
		columns, data = execute(terminal_framework._dict(no_of_interaction=1))

		# rows are lists: [lead, lead_name, company_name, reference_doctype, reference_name, content, date]
		row = next((r for r in data if r[0] == lead.name), None)
		self.assertIsNotNone(row, "seeded Lead with Received communications missing from report data")
		self.assertEqual(row[3], "Lead")
		self.assertEqual(row[4], lead.name)
		# content comes from one of the two seeded Received communications
		self.assertIn(row[5], ("_test prospect engaged 1", "_test prospect engaged 2"))

		# no_of_interaction=1 caps the per-lead communications to 1 -> exactly one row for this Lead
		lead_rows = [r for r in data if r[0] == lead.name]
		self.assertEqual(len(lead_rows), 1)
