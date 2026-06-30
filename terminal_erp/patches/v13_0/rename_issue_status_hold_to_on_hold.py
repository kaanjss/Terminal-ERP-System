# Copyright (c) 2020, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	if terminal_framework.db.exists("DocType", "Issue"):
		terminal_framework.reload_doc("support", "doctype", "issue")
		rename_status()


def rename_status():
	terminal_framework.db.sql(
		"""
		UPDATE
			`tabIssue`
		SET
			status = 'On Hold'
		WHERE
			status = 'Hold'
	"""
	)
