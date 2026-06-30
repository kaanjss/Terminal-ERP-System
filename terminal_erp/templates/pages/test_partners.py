# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework

from terminal_erp.templates.pages.partners import get_context, page_title
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestPartnersPage(Terminal ERPTestSuite):
	def _make_partner(self, name, show_in_website):
		if not terminal_framework.db.exists("Sales Partner", name):
			terminal_framework.get_doc(
				{
					"doctype": "Sales Partner",
					"partner_name": name,
					"territory": "_Test Territory",
					"commission_rate": 5,
					"show_in_website": show_in_website,
				}
			).insert(ignore_permissions=True)
		return name

	def test_get_context_lists_only_website_partners(self):
		"""partners.py builds the /partners list via
		terminal_framework.get_all("Sales Partner", filters={"show_in_website": 1}, ...).
		Seed one website-visible partner and one hidden control partner, then assert the
		returned context contains the visible one and excludes the hidden one -- real
		membership of the converted query's result, not a tautology."""
		visible = self._make_partner("_Test Website Sales Partner", 1)
		hidden = self._make_partner("_Test Hidden Sales Partner", 0)

		result = get_context(terminal_framework._dict())

		# context shape: {"partners": [...], "title": page_title}
		self.assertEqual(result["title"], page_title)
		partner_names = [p.name for p in result["partners"]]

		self.assertIn(
			visible,
			partner_names,
			"website-flagged Sales Partner missing from /partners context",
		)
		self.assertNotIn(
			hidden,
			partner_names,
			"Sales Partner with show_in_website=0 leaked into /partners context",
		)

		# every returned row really has show_in_website=1 (filter applied, not just appended)
		for partner in result["partners"]:
			self.assertEqual(
				partner.show_in_website,
				1,
				f"Sales Partner {partner.name} returned despite show_in_website != 1",
			)
