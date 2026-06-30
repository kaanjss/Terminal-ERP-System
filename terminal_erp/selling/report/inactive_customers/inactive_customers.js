// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Inactive Customers"] = {
	filters: [
		{
			fieldname: "days_since_last_order",
			label: __("Days Since Last Order"),
			fieldtype: "Int",
			default: 60,
		},
		{
			fieldname: "doctype",
			label: __("Doctype"),
			fieldtype: "Select",
			default: "Sales Order",
			options: "Sales Order\nSales Invoice",
		},
	],
};
