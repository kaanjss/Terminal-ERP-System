// Copyright (c) 2022, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.listview_settings["Subcontracting Inward Order"] = {
	get_indicator: function (doc) {
		const status_colors = {
			Draft: "red",
			Open: "orange",
			Ongoing: "yellow",
			Produced: "blue",
			Delivered: "green",
			Returned: "grey",
			Closed: "grey",
			Cancelled: "red",
		};
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	},
};
