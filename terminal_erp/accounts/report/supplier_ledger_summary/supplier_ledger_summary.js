// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Supplier Ledger Summary"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: terminal_framework.defaults.get_user_default("Company"),
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: terminal_framework.datetime.add_months(terminal_framework.datetime.get_today(), -1),
			reqd: 1,
			width: "60px",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: terminal_framework.datetime.get_today(),
			reqd: 1,
			width: "60px",
		},
		{
			fieldname: "finance_book",
			label: __("Finance Book"),
			fieldtype: "Link",
			options: "Finance Book",
		},
		{
			fieldname: "party",
			label: __("Supplier"),
			fieldtype: "Link",
			options: "Supplier",
			on_change: () => {
				var party = terminal_framework.query_report.get_filter_value("party");
				if (party) {
					terminal_framework.db.get_value("Supplier", party, ["tax_id", "supplier_name"], function (value) {
						terminal_framework.query_report.set_filter_value("tax_id", value["tax_id"]);
						terminal_framework.query_report.set_filter_value("supplier_name", value["supplier_name"]);
					});
				} else {
					terminal_framework.query_report.set_filter_value("tax_id", "");
					terminal_framework.query_report.set_filter_value("supplier_name", "");
				}
			},
		},
		{
			fieldname: "supplier_group",
			label: __("Supplier Group"),
			fieldtype: "Link",
			options: "Supplier Group",
		},
		{
			fieldname: "payment_terms_template",
			label: __("Payment Terms Template"),
			fieldtype: "Link",
			options: "Payment Terms Template",
		},
		{
			fieldname: "tax_id",
			label: __("Tax Id"),
			fieldtype: "Data",
			hidden: 1,
		},
		{
			fieldname: "supplier_name",
			label: __("Supplier Name"),
			fieldtype: "Data",
			hidden: 1,
		},
		{
			fieldname: "cost_center",
			label: __("Cost Center"),
			fieldtype: "MultiSelectList",
			options: "Cost Center",
			get_data: function (txt) {
				return terminal_framework.db.get_link_options("Cost Center", txt, {
					company: terminal_framework.query_report.get_filter_value("company"),
				});
			},
		},
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "MultiSelectList",
			options: "Project",
			get_data: function (txt) {
				return terminal_framework.db.get_link_options("Project", txt, {
					company: terminal_framework.query_report.get_filter_value("company"),
				});
			},
		},
	],
};

terminal_erp.utils.add_dimensions("Supplier Ledger Summary", 11);
