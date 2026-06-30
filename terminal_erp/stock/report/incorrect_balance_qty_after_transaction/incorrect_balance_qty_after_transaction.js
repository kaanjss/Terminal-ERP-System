// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Incorrect Balance Qty After Transaction"] = {
	filters: [
		{
			label: __("Company"),
			fieldtype: "Link",
			fieldname: "company",
			options: "Company",
			default: terminal_framework.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			label: __("Item Code"),
			fieldtype: "Link",
			fieldname: "item_code",
			options: "Item",
		},
		{
			label: __("Warehouse"),
			fieldtype: "Link",
			fieldname: "warehouse",
		},
	],
};
