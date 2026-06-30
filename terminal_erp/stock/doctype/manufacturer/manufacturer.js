// Copyright (c) 2017, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.ui.form.on("Manufacturer", {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			hide_field(["address_html", "contact_html"]);
			terminal_framework.contacts.clear_address_and_contact(frm);
		} else {
			unhide_field(["address_html", "contact_html"]);
			terminal_framework.contacts.render_address_and_contact(frm);
		}
	},
});
