// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["BOM Variance Report"] = {
	filters: [
		{
			fieldname: "bom_no",
			label: __("BOM No"),
			fieldtype: "Link",
			options: "BOM",
		},
		{
			fieldname: "work_order",
			label: __("Work Order"),
			fieldtype: "Link",
			options: "Work Order",
			get_query: function () {
				var bom_no = terminal_framework.query_report.get_filter_value("bom_no");
				return {
					query: "terminal_erp.manufacturing.report.bom_variance_report.bom_variance_report.get_work_orders",
					filters: {
						bom_no: bom_no,
					},
				};
			},
		},
	],
};
