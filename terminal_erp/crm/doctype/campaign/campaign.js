// Copyright (c) 2021, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.ui.form.on("Campaign", {
	refresh: function (frm) {
		terminal_erp.toggle_naming_series();

		if (frm.is_new()) {
			frm.toggle_display(
				"naming_series",
				terminal_framework.boot.sysdefaults.campaign_naming_by == "Naming Series"
			);
		} else {
			frm.add_custom_button(
				__("View Leads"),
				function () {
					terminal_framework.route_options = { utm_source: "Campaign", utm_campaign: frm.doc.name };
					terminal_framework.set_route("List", "Lead");
				},
				"fa fa-list",
				true
			);
		}
	},
});
