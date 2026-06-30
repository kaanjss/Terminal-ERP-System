// Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.ui.form.on("Project Update", {
	refresh: function () {},

	onload: function (frm) {
		frm.set_value("naming_series", "UPDATE-.project.-.YY.MM.DD.-.####");
	},

	validate: function (frm) {
		frm.set_value("time", terminal_framework.datetime.now_time());
		frm.set_value("date", terminal_framework.datetime.nowdate());
	},
});
