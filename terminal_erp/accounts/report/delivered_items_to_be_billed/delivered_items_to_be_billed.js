// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Delivered Items To Be Billed"] = {
	filters: [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: terminal_framework.defaults.get_default("Company"),
		},
		{
			label: __("As on Date"),
			fieldname: "posting_date",
			fieldtype: "Date",
			reqd: 1,
			default: terminal_framework.datetime.get_today(),
		},
		{
			label: __("Delivery Note"),
			fieldname: "delivery_note",
			fieldtype: "Link",
			options: "Delivery Note",
		},
	],
};
