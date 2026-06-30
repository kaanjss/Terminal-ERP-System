// Copyright (c) 2013, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Trial Balance for Party"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: terminal_framework.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: terminal_erp.utils.get_fiscal_year(terminal_framework.datetime.get_today()),
			reqd: 1,
			on_change: function (query_report) {
				var fiscal_year = query_report.get_values().fiscal_year;
				if (!fiscal_year) {
					return;
				}
				terminal_framework.model.with_doc("Fiscal Year", fiscal_year, function (r) {
					var fy = terminal_framework.model.get_doc("Fiscal Year", fiscal_year);
					terminal_framework.query_report.set_filter_value({
						from_date: fy.year_start_date,
						to_date: fy.year_end_date,
					});
				});
			},
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: terminal_erp.utils.get_fiscal_year(terminal_framework.datetime.get_today(), true)[1],
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: terminal_erp.utils.get_fiscal_year(terminal_framework.datetime.get_today(), true)[2],
		},
		{
			fieldname: "party_type",
			label: __("Party Type"),
			fieldtype: "Link",
			options: "Party Type",
			default: "Customer",
			reqd: 1,
		},
		{
			fieldname: "party",
			label: __("Party"),
			fieldtype: "Dynamic Link",
			get_options: function () {
				var party_type = terminal_framework.query_report.get_filter_value("party_type");
				var party = terminal_framework.query_report.get_filter_value("party");
				if (party && !party_type) {
					terminal_framework.throw(__("Please select Party Type first"));
				}
				return party_type;
			},
		},
		{
			fieldname: "account",
			label: __("Account"),
			fieldtype: "MultiSelectList",
			options: "Account",
			get_data: function (txt) {
				return terminal_framework.db.get_link_options("Account", txt, {
					company: terminal_framework.query_report.get_filter_value("company"),
				});
			},
		},
		{
			fieldname: "show_zero_values",
			label: __("Show zero values"),
			fieldtype: "Check",
		},
		{
			fieldname: "exclude_zero_balance_parties",
			label: __("Exclude Zero Balance Parties"),
			fieldtype: "Check",
			default: 1,
		},
	],
};
