// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.ui.form.on("Supplier", {
	setup: function (frm) {
		frm.set_query("default_price_list", { buying: 1 });
		if (frm.doc.__islocal == 1) {
			frm.set_value("represents_company", "");
		}
		frm.set_query("account", "accounts", function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: {
					account_type: "Payable",
					root_type: "Liability",
					company: d.company,
					is_group: 0,
				},
			};
		});

		frm.set_query("advance_account", "accounts", function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: {
					account_type: "Payable",
					root_type: "Asset",
					company: d.company,
					is_group: 0,
				},
			};
		});

		frm.set_query("default_bank_account", function () {
			return {
				filters: {
					is_company_account: 1,
				},
			};
		});

		frm.set_query("supplier_primary_contact", function (doc) {
			return {
				query: "terminal_erp.buying.doctype.supplier.supplier.get_supplier_primary",
				filters: {
					supplier: doc.name,
					type: "Contact",
				},
			};
		});

		frm.set_query("supplier_primary_address", function (doc) {
			return {
				query: "terminal_erp.buying.doctype.supplier.supplier.get_supplier_primary",
				filters: {
					supplier: doc.name,
					type: "Address",
				},
			};
		});

		frm.set_query("user", "portal_users", function (doc) {
			return {
				filters: {
					ignore_user_type: true,
				},
			};
		});

		frm.make_methods = {
			"Purchase Order": () =>
				terminal_framework.model.with_doctype("Purchase Order", function () {
					const po = terminal_framework.model.get_new_doc("Purchase Order");
					po.supplier = frm.doc.name;
					terminal_framework.set_route("Form", "Purchase Order", po.name);
				}),
			"Purchase Invoice": () =>
				terminal_framework.model.with_doctype("Purchase Invoice", function () {
					const pi = terminal_framework.model.get_new_doc("Purchase Invoice");
					pi.supplier = frm.doc.name;
					terminal_framework.set_route("Form", "Purchase Invoice", pi.name);
				}),
			"Request for Quotation": () =>
				terminal_framework.model.with_doctype("Request for Quotation", function () {
					const rfq = terminal_framework.model.get_new_doc("Request for Quotation");
					const row = terminal_framework.model.add_child(rfq, "suppliers");
					row.supplier = frm.doc.name;
					terminal_framework.set_route("Form", "Request for Quotation", rfq.name);
				}),
			"Supplier Quotation": () =>
				terminal_framework.model.with_doctype("Supplier Quotation", function () {
					const sq = terminal_framework.model.get_new_doc("Supplier Quotation");
					sq.supplier = frm.doc.name;
					terminal_framework.set_route("Form", "Supplier Quotation", sq.name);
				}),
			"Bank Account": () => terminal_erp.utils.make_bank_account(frm.doc.doctype, frm.doc.name),
			"Pricing Rule": () => frm.trigger("make_pricing_rule"),
		};
	},

	supplier_group(frm) {
		if (frm.doc.supplier_group) {
			frm.trigger("get_supplier_group_details");
		}
	},

	refresh: function (frm) {
		if (terminal_framework.defaults.get_default("supp_master_name") != "Naming Series") {
			frm.toggle_display("naming_series", false);
		} else {
			terminal_erp.toggle_naming_series();
		}

		if (frm.doc.__islocal) {
			hide_field(["address_html", "contact_html"]);
			terminal_framework.contacts.clear_address_and_contact(frm);
		} else {
			unhide_field(["address_html", "contact_html"]);
			terminal_framework.contacts.render_address_and_contact(frm);

			// custom buttons
			frm.add_custom_button(
				__("Accounting Ledger"),
				function () {
					terminal_framework.set_route("query-report", "General Ledger", {
						party_type: "Supplier",
						party: frm.doc.name,
						party_name: frm.doc.supplier_name,
					});
				},
				__("View")
			);

			frm.add_custom_button(
				__("Accounts Payable"),
				function () {
					terminal_framework.set_route("query-report", "Accounts Payable", {
						party_type: "Supplier",
						party: frm.doc.name,
					});
				},
				__("View")
			);

			for (const doctype in frm.make_methods) {
				frm.add_custom_button(__(doctype), frm.make_methods[doctype], __("Create"));
			}

			if (frm.doc.supplier_group) {
				frm.add_custom_button(
					__("Get Supplier Group Details"),
					function () {
						frm.trigger("get_supplier_group_details");
					},
					__("Actions")
				);
			}

			if (
				cint(terminal_framework.defaults.get_default("enable_common_party_accounting")) &&
				terminal_framework.model.can_create("Party Link")
			) {
				frm.add_custom_button(
					__("Link with Customer"),
					function () {
						frm.trigger("show_party_link_dialog");
					},
					__("Actions")
				);
			}

			// indicators
			terminal_erp.utils.set_party_dashboard_indicators(frm);
		}
	},
	get_supplier_group_details: function (frm) {
		terminal_framework.call({
			method: "get_supplier_group_details",
			doc: frm.doc,
			callback: function () {
				frm.refresh();
			},
		});
	},

	supplier_primary_address: function (frm) {
		if (frm.doc.supplier_primary_address) {
			terminal_framework.call({
				method: "terminal_framework.contacts.doctype.address.address.get_address_display",
				args: {
					address_dict: frm.doc.supplier_primary_address,
				},
				callback: function (r) {
					frm.set_value("primary_address", terminal_framework.utils.html2text(r.message));
				},
			});
		}
		if (!frm.doc.supplier_primary_address) {
			frm.set_value("primary_address", "");
		}
	},

	supplier_primary_contact: function (frm) {
		if (!frm.doc.supplier_primary_contact) {
			frm.set_value("mobile_no", "");
			frm.set_value("email_id", "");
		}
	},

	is_internal_supplier: function (frm) {
		if (frm.doc.is_internal_supplier == 1) {
			frm.toggle_reqd("represents_company", true);
		} else {
			frm.toggle_reqd("represents_company", false);
			frm.set_value("represents_company", "");
			frm.set_value("companies", []);
		}
	},
	show_party_link_dialog: function (frm) {
		const dialog = new terminal_framework.ui.Dialog({
			title: __("Select a Customer"),
			fields: [
				{
					fieldtype: "Link",
					label: __("Customer"),
					options: "Customer",
					fieldname: "customer",
					reqd: 1,
				},
			],
			primary_action: function ({ customer }) {
				terminal_framework.call({
					method: "terminal_erp.accounts.doctype.party_link.party_link.create_party_link",
					args: {
						primary_role: "Supplier",
						primary_party: frm.doc.name,
						secondary_party: customer,
					},
					freeze: true,
					callback: function () {
						dialog.hide();
						terminal_framework.msgprint({
							message: __("Successfully linked to Customer"),
							alert: true,
						});
					},
					error: function () {
						dialog.hide();
						terminal_framework.msgprint({
							message: __("Linking to Customer Failed. Please try again."),
							title: __("Linking Failed"),
							indicator: "red",
						});
					},
				});
			},
			primary_action_label: __("Create Link"),
		});
		dialog.show();
	},
	make_pricing_rule: function (frm) {
		terminal_framework.new_doc("Pricing Rule", {
			applicable_for: "Supplier",
			supplier: frm.doc.name,
			buying: 1,
		});
	},
});
