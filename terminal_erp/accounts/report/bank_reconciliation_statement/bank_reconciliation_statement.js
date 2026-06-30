// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.query_reports["Bank Reconciliation Statement"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: terminal_framework.defaults.get_user_default("Company"),
		},
		{
			fieldname: "account",
			label: __("Bank Account"),
			fieldtype: "Link",
			options: "Account",
			default: terminal_framework.defaults.get_user_default("Company")
				? locals[":Company"][terminal_framework.defaults.get_user_default("Company")]["default_bank_account"]
				: "",
			reqd: 1,
			get_query: function () {
				var company = terminal_framework.query_report.get_filter_value("company");
				return {
					query: "terminal_erp.controllers.queries.get_account_list",
					filters: [
						["Account", "account_type", "in", "Bank, Cash"],
						["Account", "is_group", "=", 0],
						["Account", "disabled", "=", 0],
						["Account", "company", "=", company],
					],
				};
			},
		},
		{
			fieldname: "report_date",
			label: __("Date"),
			fieldtype: "Date",
			default: terminal_framework.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: "include_pos_transactions",
			label: __("Include POS Transactions"),
			fieldtype: "Check",
		},
	],
	formatter: function (value, row, column, data, default_formatter, filter) {
		if (column.fieldname == "payment_entry" && value == __("Cheques and Deposits incorrectly cleared")) {
			column.link_onclick =
				"terminal_framework.query_reports['Bank Reconciliation Statement'].open_utility_report()";
		}
		return default_formatter(value, row, column, data);
	},
	open_utility_report: function () {
		terminal_framework.route_options = {
			company: terminal_framework.query_report.get_filter_value("company"),
			account: terminal_framework.query_report.get_filter_value("account"),
			report_date: terminal_framework.query_report.get_filter_value("report_date"),
		};
		terminal_framework.open_in_new_tab = true;
		terminal_framework.set_route("query-report", "Cheques and Deposits Incorrectly cleared");
	},
};
