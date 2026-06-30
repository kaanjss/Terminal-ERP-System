// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["UAE VAT 201"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: terminal_framework.defaults.get_user_default("Company"),
			get_query: function () {
				return {
					filters: {
						country: "United Arab Emirates",
					},
				};
			},
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
			default: terminal_framework.datetime.add_months(terminal_framework.datetime.get_today(), -3),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
			default: terminal_framework.datetime.get_today(),
		},
	],
	formatter: function (value, row, column, data, default_formatter) {
		if (
			data &&
			(data.legend == "VAT on Sales and All Other Outputs" ||
				data.legend == "VAT on Expenses and All Other Inputs") &&
			data.legend == value
		) {
			value = $(`<span>${value}</span>`);
			var $value = $(value).css("font-weight", "bold");
			value = $value.wrap("<p></p>").parent().html();
		}
		return value;
	},
};
