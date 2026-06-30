// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.query_reports["Budget Variance Report"] = {
	filters: get_filters(),
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname.includes(__("variance"))) {
			if (data[column.fieldname] < 0) {
				value = "<span style='color:red'>" + value + "</span>";
			} else if (data[column.fieldname] > 0) {
				value = "<span style='color:green'>" + value + "</span>";
			}
		}

		return value;
	},
};
function get_filters() {
	function get_dimensions() {
		let result = [];
		terminal_framework.call({
			method: "terminal_erp.accounts.doctype.accounting_dimension.accounting_dimension.get_dimensions",
			args: {
				with_cost_center_and_project: true,
			},
			async: false,
			callback: function (r) {
				if (!r.exc) {
					result = r.message[0].map((elem) => elem.document_type);
				}
			},
		});
		return result;
	}

	let budget_against_options = get_dimensions();

	let filters = [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: terminal_framework.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "from_fiscal_year",
			label: __("From Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: terminal_erp.utils.get_fiscal_year(terminal_framework.datetime.get_today()),
			reqd: 1,
		},
		{
			fieldname: "to_fiscal_year",
			label: __("To Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: terminal_erp.utils.get_fiscal_year(terminal_framework.datetime.get_today()),
			reqd: 1,
		},
		{
			fieldname: "period",
			label: __("Period"),
			fieldtype: "Select",
			options: [
				{ value: "Monthly", label: __("Monthly") },
				{ value: "Quarterly", label: __("Quarterly") },
				{ value: "Half-Yearly", label: __("Half-Yearly") },
				{ value: "Yearly", label: __("Yearly") },
			],
			default: "Yearly",
			reqd: 1,
		},
		{
			fieldname: "budget_against",
			label: __("Budget Against"),
			fieldtype: "Select",
			options: budget_against_options,
			default: "Cost Center",
			reqd: 1,
			on_change: function () {
				terminal_framework.query_report.set_filter_value("budget_against_filter", []);
				terminal_framework.query_report.refresh();
			},
		},
		{
			fieldname: "budget_against_filter",
			label: __("Dimension Filter"),
			fieldtype: "MultiSelectList",
			options: "budget_against",
			get_data: function (txt) {
				if (!terminal_framework.query_report.filters) return;

				let budget_against = terminal_framework.query_report.get_filter_value("budget_against");
				let company = terminal_framework.query_report.get_filter_value("company");
				if (!budget_against) return;

				const filters = budget_against !== "Branch" && company ? { company: company } : {};

				return terminal_framework.db.get_link_options(budget_against, txt, filters);
			},
		},
		{
			fieldname: "show_cumulative",
			label: __("Show Cumulative Amount"),
			fieldtype: "Check",
			default: 0,
		},
	];

	return filters;
}
