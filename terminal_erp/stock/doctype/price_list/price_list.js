// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.ui.form.on("Price List", {
	refresh: function (frm) {
		let me = this;
		frm.add_custom_button(
			__("Add / Edit Prices"),
			function () {
				terminal_framework.route_options = {
					price_list: frm.doc.name,
				};
				terminal_framework.set_route("Report", "Item Price");
			},
			"fa fa-money"
		);
	},
});
