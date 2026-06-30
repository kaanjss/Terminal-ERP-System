// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.query_reports["Customer Acquisition and Loyalty"] = {
	filters: [
		{
			fieldname: "view_type",
			label: __("View Type"),
			fieldtype: "Select",
			options: ["Monthly", "Territory Wise"],
			default: "Monthly",
			reqd: 1,
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: terminal_framework.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: terminal_erp.utils.get_fiscal_year(terminal_framework.datetime.get_today(), true)[1],
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: terminal_erp.utils.get_fiscal_year(terminal_framework.datetime.get_today(), true)[2],
			reqd: 1,
		},
	],
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.bold) {
			value = value.bold();
		}
		return value;
	},
};
