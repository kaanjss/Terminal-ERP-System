# Copyright (c) 2017, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	if terminal_framework.db.exists("Company", {"country": "India"}):
		return

	terminal_framework.reload_doc("core", "doctype", "has_role")
	terminal_framework.db.sql(
		"""
		delete from
			`tabHas Role`
		where
			parenttype = 'Report' and parent in('GST Sales Register',
				'GST Purchase Register', 'GST Itemised Sales Register',
				'GST Itemised Purchase Register', 'Eway Bill')
		"""
	)
