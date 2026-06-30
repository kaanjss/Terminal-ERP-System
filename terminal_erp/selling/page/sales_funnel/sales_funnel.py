# Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from itertools import groupby

import terminal_framework
from terminal_framework import _
from terminal_framework.query_builder.functions import Count, Date
from terminal_framework.utils import flt

from terminal_erp.accounts.report.utils import convert


def validate_filters(from_date, to_date, company):
	if from_date and to_date and (from_date >= to_date):
		terminal_framework.throw(_("To Date must be greater than From Date"))

	if not company:
		terminal_framework.throw(_("Please select a Company"))


@terminal_framework.whitelist()
def get_funnel_data(from_date: str, to_date: str, company: str):
	validate_filters(from_date, to_date, company)

	lead = terminal_framework.qb.DocType("Lead")
	active_leads = (
		terminal_framework.qb.from_(lead)
		.select(Count("*"))
		.where(Date(lead.creation).between(from_date, to_date) & (lead.company == company))
		.run()
	)[0][0]

	opportunity = terminal_framework.qb.DocType("Opportunity")
	opportunities = (
		terminal_framework.qb.from_(opportunity)
		.select(Count("*"))
		.where(
			Date(opportunity.creation).between(from_date, to_date)
			& (opportunity.opportunity_from == "Lead")
			& (opportunity.company == company)
		)
		.run()
	)[0][0]

	quotation = terminal_framework.qb.DocType("Quotation")
	quotations = (
		terminal_framework.qb.from_(quotation)
		.select(Count("*"))
		.where(
			(quotation.docstatus == 1)
			& Date(quotation.creation).between(from_date, to_date)
			& ((quotation.opportunity != "") | (quotation.quotation_to == "Lead"))
			& (quotation.company == company)
		)
		.run()
	)[0][0]

	customer = terminal_framework.qb.DocType("Customer")
	converted = (
		terminal_framework.qb.from_(customer)
		.inner_join(lead)
		.on(lead.name == customer.lead_name)
		.select(Count("*"))
		.where(Date(customer.creation).between(from_date, to_date) & (lead.company == company))
		.run()
	)[0][0]

	return [
		{"title": _("Active Leads"), "value": active_leads, "color": "#B03B46"},
		{"title": _("Opportunities"), "value": opportunities, "color": "#F09C00"},
		{"title": _("Quotations"), "value": quotations, "color": "#006685"},
		{"title": _("Converted"), "value": converted, "color": "#00AD65"},
	]


@terminal_framework.whitelist()
def get_opp_by_utm_source(from_date: str, to_date: str, company: str):
	return get_opp_by("utm_source", from_date, to_date, company)


@terminal_framework.whitelist()
def get_opp_by_utm_campaign(from_date: str, to_date: str, company: str):
	return get_opp_by("utm_campaign", from_date, to_date, company)


@terminal_framework.whitelist()
def get_opp_by_utm_medium(from_date: str, to_date: str, company: str):
	return get_opp_by("utm_medium", from_date, to_date, company)


def get_opp_by(by_field, from_date, to_date, company):
	validate_filters(from_date, to_date, company)

	opportunities = terminal_framework.get_all(
		"Opportunity",
		filters=[
			["status", "in", ["Open", "Quotation", "Replied"]],
			["company", "=", company],
			["transaction_date", "Between", [from_date, to_date]],
		],
		fields=["currency", "sales_stage", "opportunity_amount", "probability", by_field],
	)

	if opportunities:
		default_currency = terminal_framework.get_cached_value("Global Defaults", "None", "default_currency")

		cp_opportunities = [
			dict(
				x,
				**{
					"compound_amount": (
						convert(x["opportunity_amount"], x["currency"], default_currency, to_date)
						* x["probability"]
						/ 100
					)
				},
			)
			for x in opportunities
			if x.get(by_field)
		]

		summary = {}
		sales_stages = set()
		group_key = lambda o: (o[by_field], o["sales_stage"])  # noqa
		for (by_field_group, sales_stage), rows in groupby(
			sorted(cp_opportunities, key=group_key), group_key
		):
			summary.setdefault(by_field_group, {})[sales_stage] = sum(r["compound_amount"] for r in rows)
			sales_stages.add(sales_stage)

		pivot_table = []
		for sales_stage in sales_stages:
			row = []
			for sales_stage_values in summary.values():
				row.append(flt(sales_stage_values.get(sales_stage)))
			pivot_table.append({"chartType": "bar", "name": sales_stage, "values": row})

		result = {"datasets": pivot_table, "labels": list(summary.keys())}
		return result

	else:
		return "empty"


@terminal_framework.whitelist()
def get_pipeline_data(from_date: str, to_date: str, company: str):
	validate_filters(from_date, to_date, company)

	opportunities = terminal_framework.get_all(
		"Opportunity",
		filters=[
			["status", "in", ["Open", "Quotation", "Replied"]],
			["company", "=", company],
			["transaction_date", "Between", [from_date, to_date]],
		],
		fields=["currency", "sales_stage", "opportunity_amount", "probability"],
	)

	if opportunities:
		default_currency = terminal_framework.get_cached_value("Global Defaults", "None", "default_currency")

		cp_opportunities = [
			dict(
				x,
				**{
					"compound_amount": (
						convert(x["opportunity_amount"], x["currency"], default_currency, to_date)
						* x["probability"]
						/ 100
					)
				},
			)
			for x in opportunities
		]

		summary = {}
		for sales_stage, rows in groupby(cp_opportunities, lambda o: o["sales_stage"]):
			summary[sales_stage] = sum(flt(r["compound_amount"]) for r in rows)

		result = {
			"labels": list(summary.keys()),
			"datasets": [{"name": _("Total Amount"), "values": list(summary.values()), "chartType": "bar"}],
		}
		return result

	else:
		return "empty"
