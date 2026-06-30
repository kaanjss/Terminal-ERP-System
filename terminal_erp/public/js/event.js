// Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt
terminal_framework.provide("terminal_framework.desk");

terminal_framework.ui.form.on("Event", {
	refresh: function (frm) {
		frm.set_query("reference_doctype", "event_participants", function () {
			return {
				filters: {
					name: ["in", ["Contact", "Lead", "Customer", "Supplier", "Employee", "Sales Partner"]],
				},
			};
		});

		frm.add_custom_button(
			__("Add Leads"),
			function () {
				new terminal_framework.desk.eventParticipants(frm, "Lead");
			},
			__("Add Participants")
		);

		frm.add_custom_button(
			__("Add Customers"),
			function () {
				new terminal_framework.desk.eventParticipants(frm, "Customer");
			},
			__("Add Participants")
		);

		frm.add_custom_button(
			__("Add Suppliers"),
			function () {
				new terminal_framework.desk.eventParticipants(frm, "Supplier");
			},
			__("Add Participants")
		);

		frm.add_custom_button(
			__("Add Employees"),
			function () {
				new terminal_framework.desk.eventParticipants(frm, "Employee");
			},
			__("Add Participants")
		);

		frm.add_custom_button(
			__("Add Sales Partners"),
			function () {
				new terminal_framework.desk.eventParticipants(frm, "Sales Partner");
			},
			__("Add Participants")
		);
	},
});
