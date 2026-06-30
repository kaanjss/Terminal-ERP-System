terminal_framework.provide("terminal_erp.demo");

$(document).on("desktop_screen", function (event, data) {
	data.desktop.add_menu_item({
		label: __("Delete Demo Data"),
		icon: "trash",
		condition: function () {
			return terminal_framework.boot.sysdefaults.demo_company;
		},
		onClick: function () {
			return terminal_erp.demo.clear_demo();
		},
	});
});

terminal_erp.demo.clear_demo = function () {
	terminal_framework.confirm(__("Are you sure you want to clear all demo data?"), () => {
		terminal_framework.call({
			method: "terminal_erp.setup.demo.clear_demo_data",
			freeze: true,
			freeze_message: __("Clearing Demo Data..."),
			callback: function (r) {
				terminal_framework.ui.toolbar.clear_cache();
				terminal_framework.show_alert({
					message: __("Demo data cleared"),
					indicator: "green",
				});
			},
		});
	});
};
