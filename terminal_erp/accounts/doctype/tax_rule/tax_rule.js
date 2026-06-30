// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.ui.form.on("Tax Rule", "customer", function (frm) {
	if (frm.doc.customer) {
		terminal_framework.call({
			method: "terminal_erp.accounts.doctype.tax_rule.tax_rule.get_party_details",
			args: {
				party: frm.doc.customer,
				party_type: "customer",
			},
			callback: function (r) {
				if (!r.exc) {
					$.each(r.message, function (k, v) {
						frm.set_value(k, v);
					});
				}
			},
		});
	}
});

terminal_framework.ui.form.on("Tax Rule", "supplier", function (frm) {
	if (frm.doc.supplier) {
		terminal_framework.call({
			method: "terminal_erp.accounts.doctype.tax_rule.tax_rule.get_party_details",
			args: {
				party: frm.doc.supplier,
				party_type: "supplier",
			},
			callback: function (r) {
				if (!r.exc) {
					$.each(r.message, function (k, v) {
						frm.set_value(k, v);
					});
				}
			},
		});
	}
});
