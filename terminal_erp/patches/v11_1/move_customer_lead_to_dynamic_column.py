# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doctype("Quotation")
	terminal_framework.db.sql(""" UPDATE `tabQuotation` set party_name = lead WHERE quotation_to = 'Lead' """)
	terminal_framework.db.sql(""" UPDATE `tabQuotation` set party_name = customer WHERE quotation_to = 'Customer' """)

	terminal_framework.reload_doctype("Opportunity")
	terminal_framework.db.sql(""" UPDATE `tabOpportunity` set party_name = lead WHERE opportunity_from = 'Lead' """)
	terminal_framework.db.sql(
		""" UPDATE `tabOpportunity` set party_name = customer WHERE opportunity_from = 'Customer' """
	)
