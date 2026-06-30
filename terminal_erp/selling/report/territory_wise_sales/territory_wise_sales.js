// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Territory-wise Sales"] = {
	breadcrumb: "Selling",
	filters: [
		{
			fieldname: "transaction_date",
			label: __("Transaction Date"),
			fieldtype: "DateRange",
			default: [
				terminal_framework.datetime.add_months(terminal_framework.datetime.get_today(), -1),
				terminal_framework.datetime.get_today(),
			],
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
		},
	],
};
