terminal_framework.pages["visual-plant-floor"].on_page_load = function (wrapper) {
	var page = terminal_framework.ui.make_app_page({
		parent: wrapper,
		title: "Visual Plant Floor",
		single_column: true,
	});

	terminal_framework.visual_plant_floor = new terminal_framework.ui.VisualPlantFloor(
		{ wrapper: $(wrapper).find(".layout-main-section") },
		wrapper.page
	);
};
