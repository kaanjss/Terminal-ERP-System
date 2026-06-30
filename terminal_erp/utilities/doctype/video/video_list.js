terminal_framework.listview_settings["Video"] = {
	onload: (listview) => {
		listview.page.add_menu_item(__("Video Settings"), function () {
			terminal_framework.set_route("Form", "Video Settings", "Video Settings");
		});
	},
};
