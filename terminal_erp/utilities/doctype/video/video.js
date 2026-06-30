// Copyright (c) 2020, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.ui.form.on("Video", {
	refresh: function (frm) {
		frm.events.toggle_youtube_statistics_section(frm);
		frm.add_custom_button(__("Watch Video"), () => terminal_framework.help.show_video(frm.doc.url, frm.doc.title));
	},

	toggle_youtube_statistics_section: (frm) => {
		if (frm.doc.provider === "YouTube") {
			terminal_framework.db.get_single_value("Video Settings", "enable_youtube_tracking").then((val) => {
				frm.toggle_display("youtube_tracking_section", val);
			});
		}
	},
});
