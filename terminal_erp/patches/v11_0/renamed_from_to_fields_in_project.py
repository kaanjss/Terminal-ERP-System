# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	terminal_framework.reload_doc("projects", "doctype", "project")

	if terminal_framework.db.has_column("Project", "from"):
		rename_field("Project", "from", "from_time")
		rename_field("Project", "to", "to_time")
