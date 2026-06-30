// Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Incorrect Serial and Batch Bundle"] = {
	filters: [
		{
			fieldname: "item_code",
			label: __("Item Code"),
			fieldtype: "Link",
			options: "Item",
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
		},
	],

	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},

	onload(report) {
		report.page
			.add_inner_button(__("Fix SABB Entry"), () => {
				let indexes = terminal_framework.query_report.datatable.rowmanager.getCheckedRows();
				let selected_rows = indexes.map((i) => terminal_framework.query_report.data[i]);

				if (!selected_rows.length) {
					terminal_framework.throw(__("Please select at least one row to fix"));
				} else {
					terminal_framework.call({
						method: "terminal_erp.stock.report.incorrect_serial_and_batch_bundle.incorrect_serial_and_batch_bundle.fix_sabb_entries",
						freeze: true,
						args: {
							selected_rows: selected_rows,
						},
						callback: function (r) {
							terminal_framework.query_report.refresh();
						},
					});
				}
			})
			.addClass("btn-primary");
	},
};
