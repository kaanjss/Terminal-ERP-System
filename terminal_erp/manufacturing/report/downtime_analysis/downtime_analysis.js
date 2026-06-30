// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Downtime Analysis"] = {
	filters: [
		{
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Datetime",
			default: terminal_framework.datetime.convert_to_system_tz(
				terminal_framework.datetime.add_months(terminal_framework.datetime.now_datetime(), -1)
			),
			reqd: 1,
		},
		{
			label: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Datetime",
			default: terminal_framework.datetime.now_datetime(),
			reqd: 1,
		},
		{
			label: __("Machine"),
			fieldname: "workstation",
			fieldtype: "Link",
			options: "Workstation",
		},
	],
};
