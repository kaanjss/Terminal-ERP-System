# Copyright (c) 2017, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("setup", "doctype", "target_detail")
	terminal_framework.reload_doc("core", "doctype", "prepared_report")

	for d in ["Sales Person", "Sales Partner", "Territory"]:
		terminal_framework.db.sql(
			"""
            UPDATE `tab{child_doc}`, `tab{parent_doc}`
            SET
                `tab{child_doc}`.distribution_id = `tab{parent_doc}`.distribution_id
            WHERE
                `tab{child_doc}`.parent = `tab{parent_doc}`.name
                and `tab{parent_doc}`.distribution_id is not null and `tab{parent_doc}`.distribution_id != ''
        """.format(parent_doc=d, child_doc="Target Detail")
		)

	terminal_framework.delete_doc("Report", "Sales Partner-wise Transaction Summary")
	terminal_framework.delete_doc("Report", "Sales Person Target Variance Item Group-Wise")
	terminal_framework.delete_doc("Report", "Territory Target Variance Item Group-Wise")
