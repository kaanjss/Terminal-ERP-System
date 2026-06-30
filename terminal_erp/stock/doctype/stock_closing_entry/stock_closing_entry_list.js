terminal_framework.listview_settings["Stock Closing Entry"] = {
	add_fields: ["status"],
	get_indicator: function (doc) {
		return [__(doc.status), terminal_framework.utils.guess_colour(doc.status), "status,=," + doc.status];
	},
};
