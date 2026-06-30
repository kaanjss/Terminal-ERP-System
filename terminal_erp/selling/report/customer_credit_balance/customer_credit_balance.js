// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Customer Credit Balance"] = {
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
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
	],
};
