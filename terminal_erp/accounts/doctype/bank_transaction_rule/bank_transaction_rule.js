// Copyright (c) 2026, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.ui.form.on("Bank Transaction Rule", {
	refresh: function (frm) {
		frm.set_query("account", function () {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});

		frm.set_intro(
			__(
				"Go to the <a href='/banking' target='_blank' style='text-decoration: underline;'>Banking module</a> to setup this rule."
			)
		);
	},
});
