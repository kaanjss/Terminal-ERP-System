// Copyright (c) 2019, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.ui.form.on("Project Template", {
	// refresh: function(frm) {

	// }
	setup: function (frm) {
		frm.set_query("task", "tasks", function () {
			return {
				filters: {
					is_template: 1,
				},
			};
		});
	},
});

terminal_framework.ui.form.on("Project Template Task", {
	task: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];

		if (!row.task) {
			row.subject = null;
			refresh_field("tasks");
			return;
		}

		terminal_framework.db.get_value("Task", row.task, "subject", (value) => {
			row.subject = value.subject;
			refresh_field("tasks");
		});
	},
});
