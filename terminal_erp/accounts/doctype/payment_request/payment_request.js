cur_frm.add_fetch("payment_gateway_account", "payment_account", "payment_account");
cur_frm.add_fetch("payment_gateway_account", "payment_gateway", "payment_gateway");
cur_frm.add_fetch("payment_gateway_account", "message", "message");

terminal_framework.ui.form.on("Payment Request", {
	setup: function (frm) {
		frm.set_query("party_type", function () {
			return {
				query: "terminal_erp.setup.doctype.party_type.party_type.get_party_type",
			};
		});

		frm.set_query("payment_gateway_account", function () {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});
	},
});

terminal_framework.ui.form.on("Payment Request", "onload", function (frm, dt, dn) {
	if (frm.doc.reference_doctype) {
		terminal_framework.call({
			method: "terminal_erp.accounts.doctype.payment_request.payment_request.get_print_format_list",
			args: { ref_doctype: frm.doc.reference_doctype },
			callback: function (r) {
				set_field_options("print_format", r.message["print_format"]);
			},
		});
	}
});

terminal_framework.ui.form.on("Payment Request", "refresh", function (frm) {
	if (frm.doc.status == "Failed") {
		frm.set_intro(__("Failure: {0}", [frm.doc.failed_reason]), "red");
	}

	if (
		frm.doc.payment_request_type == "Inward" &&
		frm.doc.payment_channel !== "Phone" &&
		!["Initiated", "Paid"].includes(frm.doc.status) &&
		!frm.doc.__islocal &&
		frm.doc.docstatus == 1
	) {
		frm.add_custom_button(__("Resend Payment Email"), function () {
			terminal_framework.call({
				method: "terminal_erp.accounts.doctype.payment_request.payment_request.resend_payment_email",
				args: { docname: frm.doc.name },
				freeze: true,
				freeze_message: __("Sending"),
				callback: function (r) {
					if (!r.exc) {
						terminal_framework.msgprint(__("Message Sent"));
					}
				},
			});
		});
	}

	if (
		frm.doc.payment_request_type == "Outward" &&
		["Initiated", "Partially Paid"].includes(frm.doc.status)
	) {
		frm.add_custom_button(__("Create Payment Entry"), function () {
			terminal_framework.call({
				method: "terminal_erp.accounts.doctype.payment_request.payment_request.make_payment_entry",
				args: { docname: frm.doc.name },
				freeze: true,
				callback: function (r) {
					if (!r.exc) {
						var doc = terminal_framework.model.sync(r.message);
						terminal_framework.set_route("Form", r.message.doctype, r.message.name);
					}
				},
			});
		}).addClass("btn-primary");
	}
});

terminal_framework.ui.form.on("Payment Request", "is_a_subscription", function (frm) {
	frm.toggle_reqd("payment_gateway_account", frm.doc.is_a_subscription);
	frm.toggle_reqd("subscription_plans", frm.doc.is_a_subscription);

	if (frm.doc.is_a_subscription && frm.doc.reference_doctype && frm.doc.reference_name) {
		terminal_framework.call({
			method: "terminal_erp.accounts.doctype.payment_request.payment_request.get_subscription_details",
			args: { reference_doctype: frm.doc.reference_doctype, reference_name: frm.doc.reference_name },
			freeze: true,
			callback: function (data) {
				if (!data.exc) {
					$.each(data.message || [], function (i, v) {
						var d = terminal_framework.model.add_child(
							frm.doc,
							"Subscription Plan Detail",
							"subscription_plans"
						);
						d.qty = v.qty;
						d.plan = v.plan;
					});
					frm.refresh_field("subscription_plans");
				}
			},
		});
	}
});

terminal_framework.ui.form.on("Payment Request", "calculate_total_amount_by_selected_rows", function (frm) {
	if (frm.doc.docstatus !== 0) {
		terminal_framework.msgprint(__("Cannot fetch selected rows for submitted Payment Request"));
		return;
	}
	const selected = frm.get_selected()?.payment_reference || [];
	if (!selected.length) {
		terminal_framework.throw(__("No rows selected"));
	}
	let total = 0;
	selected.forEach((name) => {
		const row = frm.doc.payment_reference.find((d) => d.name === name);
		if (row) {
			row.manually_selected = 1;

			total += row.amount;
		}
	});
	frm.doc.payment_reference.forEach((row) => {
		row.auto_selected = 0;
	});
	frm.set_value("grand_total", total);
	frm.refresh_field("grand_total");
	frm.save();
});
