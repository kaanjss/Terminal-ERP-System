// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.views.calendar["Task"] = {
	field_map: {
		start: "exp_start_date",
		end: "exp_end_date",
		id: "name",
		title: "subject",
		allDay: "allDay",
		progress: "progress",
	},
	gantt: true,
	filters: [
		{
			fieldtype: "Link",
			fieldname: "project",
			options: "Project",
			label: __("Project"),
		},
	],
	get_events_method: "terminal_framework.desk.calendar.get_events",
};
