// Copyright (c) 2023, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.ui.form.on("Bulk Transaction Log", {
	refresh(frm) {
		frm.add_custom_button(
			__("Succeeded Entries"),
			function () {
				terminal_framework.set_route("List", "Bulk Transaction Log Detail", {
					date: frm.doc.date,
					transaction_status: "Success",
				});
			},
			__("View")
		);
		frm.add_custom_button(
			__("Failed Entries"),
			function () {
				terminal_framework.set_route("List", "Bulk Transaction Log Detail", {
					date: frm.doc.date,
					transaction_status: "Failed",
				});
			},
			__("View")
		);
		if (frm.doc.failed) {
			frm.add_custom_button(__("Retry Failed Transactions"), function () {
				terminal_framework.call({
					method: "terminal_erp.utilities.bulk_transaction.retry",
					args: { date: frm.doc.date },
				});
			});
		}
	},
});
