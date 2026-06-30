// Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.ui.form.on("Bank Account", {
	setup: function (frm) {
		frm.set_query("account", function () {
			return {
				filters: {
					account_type: "Bank",
					company: frm.doc.company,
					is_group: 0,
				},
			};
		});
		frm.set_query("party_type", function () {
			return {
				query: "terminal_erp.setup.doctype.party_type.party_type.get_party_type",
			};
		});
	},
	refresh: function (frm) {
		terminal_framework.dynamic_link = { doc: frm.doc, fieldname: "name", doctype: "Bank Account" };

		frm.toggle_display(["address_html", "contact_html"], !frm.doc.__islocal);

		if (frm.doc.__islocal) {
			terminal_framework.contacts.clear_address_and_contact(frm);
		} else {
			terminal_framework.contacts.render_address_and_contact(frm);
		}

		if (frm.doc.integration_id) {
			frm.add_custom_button(__("Unlink external integrations"), function () {
				terminal_framework.confirm(
					__(
						"This action will unlink this account from any external service integrating Terminal ERP with your bank accounts. It cannot be undone. Are you certain ?"
					),
					function () {
						frm.set_value("integration_id", "");
					}
				);
			});
		}
	},
});
