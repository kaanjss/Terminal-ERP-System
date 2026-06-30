// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Process Loss Report"] = {
	filters: [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			mandatory: true,
			default: terminal_framework.defaults.get_user_default("Company"),
		},
		{
			label: __("Item"),
			fieldname: "item",
			fieldtype: "Link",
			options: "Item",
			mandatory: false,
		},
		{
			label: __("Work Order"),
			fieldname: "work_order",
			fieldtype: "Link",
			options: "Work Order",
			mandatory: false,
		},
		{
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			mandatory: true,
			default: terminal_framework.datetime.year_start(),
		},
		{
			label: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Date",
			mandatory: true,
			default: terminal_framework.datetime.get_today(),
		},
	],
};
