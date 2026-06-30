import terminal_framework


def execute():
	terminal_framework.reload_doctype("Opportunity")
	if terminal_framework.db.has_column("Opportunity", "enquiry_from"):
		terminal_framework.db.sql(
			""" UPDATE `tabOpportunity` set opportunity_from = enquiry_from
			where ifnull(opportunity_from, '') = '' and ifnull(enquiry_from, '') != ''"""
		)

	if terminal_framework.db.has_column("Opportunity", "lead") and terminal_framework.db.has_column("Opportunity", "enquiry_from"):
		terminal_framework.db.sql(
			""" UPDATE `tabOpportunity` set party_name = lead
			where enquiry_from = 'Lead' and ifnull(party_name, '') = '' and ifnull(lead, '') != ''"""
		)

	if terminal_framework.db.has_column("Opportunity", "customer") and terminal_framework.db.has_column(
		"Opportunity", "enquiry_from"
	):
		terminal_framework.db.sql(
			""" UPDATE `tabOpportunity` set party_name = customer
			 where enquiry_from = 'Customer' and ifnull(party_name, '') = '' and ifnull(customer, '') != ''"""
		)
