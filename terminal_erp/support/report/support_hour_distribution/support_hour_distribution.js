// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Support Hour Distribution"] = {
	filters: [
		{
			lable: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			default: terminal_framework.datetime.nowdate(),
			reqd: 1,
		},
		{
			lable: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Date",
			default: terminal_framework.datetime.nowdate(),
			reqd: 1,
		},
	],
};
