// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.provide("terminal_erp.support");

terminal_framework.ui.form.on("Warranty Claim", {
	setup: (frm) => {
		frm.set_query("contact_person", terminal_erp.queries.contact_query);
		frm.set_query("customer_address", terminal_erp.queries.address_query);
		frm.set_query("customer", terminal_erp.queries.customer);

		frm.set_query("serial_no", () => {
			let filters = {
				company: frm.doc.company,
			};

			if (frm.doc.item_code) {
				filters["item_code"] = frm.doc.item_code;
			}

			return { filters: filters };
		});

		frm.set_query("item_code", () => {
			return {
				filters: {
					disabled: 0,
				},
			};
		});
	},

	onload: (frm) => {
		if (!frm.doc.status) {
			frm.set_value("status", "Open");
		}
	},

	refresh: (frm) => {
		terminal_framework.dynamic_link = {
			doc: frm.doc,
			fieldname: "customer",
			doctype: "Customer",
		};

		if (!frm.doc.__islocal && ["Open", "Work In Progress"].includes(frm.doc.status)) {
			frm.add_custom_button(__("Maintenance Visit"), () => {
				terminal_framework.model.open_mapped_doc({
					method: "terminal_erp.support.doctype.warranty_claim.warranty_claim.make_maintenance_visit",
					frm: frm,
				});
			});
		}
	},

	customer: (frm) => {
		terminal_erp.utils.get_party_details(frm);
	},

	customer_address: (frm) => {
		terminal_erp.utils.get_address_display(frm);
	},

	contact_person: (frm) => {
		terminal_erp.utils.get_contact_details(frm);
	},
});
