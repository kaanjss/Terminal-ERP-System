// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.ui.form.on("Email Digest", {
	refresh: function (frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("View Now"), function () {
				terminal_framework.call({
					method: "terminal_erp.setup.doctype.email_digest.email_digest.get_digest_msg",
					args: {
						name: frm.doc.name,
					},
					callback: function (r) {
						let d = new terminal_framework.ui.Dialog({
							title: __("Email Digest: {0}", [frm.doc.name]),
							width: 800,
						});
						$(d.body).html(r.message);
						d.show();
					},
				});
			});

			frm.add_custom_button(__("Send Now"), function () {
				return frm.call("send", null, () => {
					terminal_framework.show_alert({ message: __("Message Sent"), indicator: "green" });
				});
			});
		}
	},
});
