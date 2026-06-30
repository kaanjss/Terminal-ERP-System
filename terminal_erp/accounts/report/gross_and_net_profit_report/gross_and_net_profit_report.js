// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

const GNP_REPORT = "Gross and Net Profit Report";

terminal_framework.query_reports[GNP_REPORT] = $.extend({}, terminal_erp.financial_statements);

terminal_erp.utils.add_dimensions(GNP_REPORT, 10);

terminal_framework.query_reports[GNP_REPORT]["filters"].push({
	fieldname: "accumulated_values",
	label: __("Accumulated Values"),
	fieldtype: "Check",
});
