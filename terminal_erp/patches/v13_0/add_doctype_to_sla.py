# Copyright (c) 2020, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	terminal_framework.reload_doc("support", "doctype", "sla_fulfilled_on_status")
	terminal_framework.reload_doc("support", "doctype", "service_level_agreement")
	if terminal_framework.db.has_column("Service Level Agreement", "enable"):
		rename_field("Service Level Agreement", "enable", "enabled")

	for sla in terminal_framework.get_all("Service Level Agreement"):
		agreement = terminal_framework.get_doc("Service Level Agreement", sla.name)
		agreement.db_set("document_type", "Issue")
		agreement.reload()
		agreement.apply_sla_for_resolution = 1
		agreement.append("sla_fulfilled_on", {"status": "Resolved"})
		agreement.append("sla_fulfilled_on", {"status": "Closed"})
		agreement.save()
