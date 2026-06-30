// Copyright (c) 2016, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.query_reports["Item Prices"] = {
	filters: [
		{
			fieldname: "items",
			label: __("Items Filter"),
			fieldtype: "Select",
			options: "Enabled Items only\nDisabled Items only\nAll Items",
			default: "Enabled Items only",
		},
	],
};
