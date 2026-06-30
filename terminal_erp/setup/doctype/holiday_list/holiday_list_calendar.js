// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.views.calendar["Holiday List"] = {
	field_map: {
		start: "holiday_date",
		end: "holiday_date",
		id: "name",
		title: "description",
		allDay: "allDay",
	},
	order_by: `from_date`,
	get_events_method: "terminal_erp.setup.doctype.holiday_list.holiday_list.get_events",
	filters: [
		{
			fieldtype: "Link",
			fieldname: "holiday_list",
			options: "Holiday List",
			label: __("Holiday List"),
		},
	],
};
