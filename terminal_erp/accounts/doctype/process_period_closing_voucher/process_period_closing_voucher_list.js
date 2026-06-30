// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// render
terminal_framework.listview_settings["Process Period Closing Voucher"] = {
	add_fields: ["status"],
	get_indicator: function (doc) {
		const status_colors = {
			Queued: "blue",
			Running: "orange",
			Paused: "gray",
			Completed: "green",
			Cancelled: "red",
		};
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	},
};
