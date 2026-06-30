// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
terminal_framework.query_reports["Lead Owner Efficiency"] = {
	filters: [
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
	],
};
