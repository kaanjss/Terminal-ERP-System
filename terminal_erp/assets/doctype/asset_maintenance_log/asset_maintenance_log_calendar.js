// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.views.calendar["Asset Maintenance Log"] = {
	field_map: {
		start: "due_date",
		end: "due_date",
		id: "name",
		title: "task",
		allDay: "allDay",
		progress: "progress",
	},
	filters: [
		{
			fieldtype: "Link",
			fieldname: "asset_name",
			options: "Asset Maintenance",
			label: __("Asset Maintenance"),
		},
	],
	get_events_method: "terminal_framework.desk.calendar.get_events",
};
