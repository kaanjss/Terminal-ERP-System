// Copyright (c) 2023, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Lost Quotations"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: terminal_framework.defaults.get_user_default("Company"),
		},
		{
			label: "Timespan",
			fieldtype: "Select",
			fieldname: "timespan",
			options: [
				"Last Week",
				"Last Month",
				"Last Quarter",
				"Last 6 months",
				"Last Year",
				"This Week",
				"This Month",
				"This Quarter",
				"This Year",
			],
			default: "This Year",
			reqd: 1,
		},
		{
			fieldname: "group_by",
			label: __("Group By"),
			fieldtype: "Select",
			options: ["Lost Reason", "Competitor"],
			default: "Lost Reason",
			reqd: 1,
		},
	],
};
