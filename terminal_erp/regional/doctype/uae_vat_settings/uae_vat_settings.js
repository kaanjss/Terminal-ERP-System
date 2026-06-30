// Copyright (c) 2020, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.ui.form.on("UAE VAT Settings", {
	onload: function (frm) {
		frm.set_query("account", "uae_vat_accounts", function () {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});
	},
});
