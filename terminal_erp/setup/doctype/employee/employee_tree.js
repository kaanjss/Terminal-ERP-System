terminal_framework.treeview_settings["Employee"] = {
	get_tree_nodes: "terminal_erp.setup.doctype.employee.employee.get_children",
	filters: [
		{
			fieldname: "company",
			fieldtype: "Select",
			options: ["All Companies"].concat(terminal_erp.utils.get_tree_options("company")),
			label: __("Company"),
			default: terminal_erp.utils.get_tree_default("company"),
		},
	],
	breadcrumb: "Hr",
	disable_add_node: true,
	get_tree_root: false,
	toolbar: [
		{ toggle_btn: true },
		{
			label: __("Edit"),
			condition: function (node) {
				return !node.is_root;
			},
			click: function (node) {
				terminal_framework.set_route("Form", "Employee", node.data.value);
			},
		},
	],
	menu_items: [
		{
			label: __("New Employee"),
			action: function () {
				terminal_framework.new_doc("Employee", true);
			},
			condition: 'terminal_framework.boot.user.can_create.indexOf("Employee") !== -1',
		},
	],
};
