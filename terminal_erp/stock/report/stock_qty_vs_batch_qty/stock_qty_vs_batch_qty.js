// Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Stock Qty vs Batch Qty"] = {
	filters: [
		{
			fieldname: "item",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
			get_query: function () {
				return {
					filters: { has_batch_no: true },
				};
			},
		},
		{
			fieldname: "batch",
			label: __("Batch"),
			fieldtype: "Link",
			options: "Batch",
			get_query: function () {
				const item_code = terminal_framework.query_report.get_filter_value("item");
				return {
					filters: { item: item_code, disabled: 0 },
				};
			},
		},
	],
	onload: function (report) {
		if (terminal_framework.model.can_write("Batch")) {
			report.page.add_inner_button(__("Update Batch Qty"), function () {
				let indexes = terminal_framework.query_report.datatable.rowmanager.getCheckedRows();
				let selected_rows = indexes
					.map((i) => terminal_framework.query_report.data[i])
					.filter((row) => row.difference != 0);

				if (selected_rows.length) {
					terminal_framework.call({
						method: "terminal_erp.stock.report.stock_qty_vs_batch_qty.stock_qty_vs_batch_qty.update_batch_qty",
						args: {
							selected_batches: selected_rows,
						},
						callback: function (r) {
							if (!r.exc) {
								report.refresh();
							}
						},
					});
				} else {
					terminal_framework.msgprint(__("Please select at least one row with difference value"));
				}
			});
		}
	},

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname == "difference" && data) {
			if (data.difference > 0) {
				value = "<span style='color:red'>" + value + "</span>";
			} else if (data.difference < 0) {
				value = "<span style='color:red'>" + value + "</span>";
			}
		}
		return value;
	},
	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},
};
