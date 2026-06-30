// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["VAT Audit Report"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: terminal_framework.defaults.get_user_default("Company"),
			get_query: function () {
				return {
					filters: {
						country: "South Africa",
					},
				};
			},
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
			default: terminal_framework.datetime.add_months(terminal_framework.datetime.get_today(), -2),
			width: "80",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
			default: terminal_framework.datetime.get_today(),
		},
	],
};
