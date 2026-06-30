terminal_framework.provide("terminal_erp.PointOfSale");

terminal_framework.pages["point-of-sale"].on_page_load = function (wrapper) {
	terminal_framework.ui.make_app_page({
		parent: wrapper,
		title: __("Point of Sale"),
		single_column: true,
		hide_sidebar: true,
	});

	terminal_framework.require("point-of-sale.bundle.js", function () {
		wrapper.pos = new terminal_erp.PointOfSale.Controller(wrapper);
		window.cur_pos = wrapper.pos;
	});
};

terminal_framework.pages["point-of-sale"].refresh = function (wrapper) {
	if (document.scannerDetectionData) {
		onScan.detachFrom(document);
		wrapper.pos.wrapper.html("");
		wrapper.pos.check_opening_entry();
	}
};
