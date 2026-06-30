// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Address And Contacts"] = {
	filters: [
		{
			reqd: 1,
			fieldname: "party_type",
			label: __("Party Type"),
			fieldtype: "Link",
			options: "DocType",
			get_query: function () {
				return {
					filters: {
						name: ["in", "Customer,Supplier,Sales Partner,Lead"],
					},
				};
			},
		},
		{
			fieldname: "party_name",
			label: __("Party Name"),
			fieldtype: "Dynamic Link",
			get_options: function () {
				let party_type = terminal_framework.query_report.get_filter_value("party_type");
				if (!party_type) {
					terminal_framework.throw(__("Please select Party Type first"));
				}
				return party_type;
			},
		},
	],
};
