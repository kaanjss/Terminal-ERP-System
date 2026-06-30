// Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

const CFS_REPORT_NAME = "Custom Financial Statement";

terminal_framework.query_reports[CFS_REPORT_NAME] = $.extend({}, terminal_erp.financial_statements);

terminal_erp.utils.add_dimensions(CFS_REPORT_NAME, 10);

terminal_framework.query_reports[CFS_REPORT_NAME]["filters"].push(
	{
		fieldname: "report_template",
		label: __("Report Template"),
		fieldtype: "Link",
		options: "Financial Report Template",
		get_query: { filters: { disabled: 0 } },
		reqd: 1,
	},
	{
		fieldname: "show_account_details",
		label: __("Account Detail Level"),
		fieldtype: "Select",
		options: ["Summary", "Account Breakdown"],
		default: "Summary",
		depends_on: "eval:doc.report_template",
	},
	{
		fieldname: "include_default_book_entries",
		label: __("Include Default FB Entries"),
		fieldtype: "Check",
		default: 1,
	}
);

terminal_framework.query_reports[CFS_REPORT_NAME]["export_hidden_cols"] = true;
