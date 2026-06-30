// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Stock and Account Value Comparison"] = {
	filters: [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: terminal_framework.defaults.get_user_default("Company"),
		},
		{
			label: __("Account"),
			fieldname: "account",
			fieldtype: "Link",
			options: "Account",
			get_query: function () {
				var company = terminal_framework.query_report.get_filter_value("company");
				return {
					filters: {
						account_type: "Stock",
						company: company,
					},
				};
			},
		},
		{
			label: __("As On Date"),
			fieldname: "as_on_date",
			fieldtype: "Date",
			default: terminal_framework.datetime.get_today(),
		},
	],

	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},

	onload(report) {
		report.page.add_inner_button(__("Create Reposting Entries"), function () {
			let message = `<div>
				<p>
					${__(
						"Reposting Entries will change the value of accounts Stock In Hand, and Stock Expenses in the Trial Balance report and will also change the Balance Value in the Stock Balance report."
					)}
				</p>
				<p>${__("Are you sure you want to create Reposting Entries?")}</p>
				</div>
			`;
			let indexes = terminal_framework.query_report.datatable.rowmanager.getCheckedRows();
			let selected_rows = indexes.map((i) => terminal_framework.query_report.data[i]);

			if (!selected_rows.length) {
				terminal_framework.throw(__("Please select rows to create Reposting Entries"));
			}

			terminal_framework.confirm(message, () => {
				terminal_framework.call({
					method: "terminal_erp.stock.report.stock_and_account_value_comparison.stock_and_account_value_comparison.create_reposting_entries",
					args: {
						rows: selected_rows,
						company: terminal_framework.query_report.get_filter_values().company,
					},
				});
			});
		});
	},
};
