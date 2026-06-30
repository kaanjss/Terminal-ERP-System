terminal_framework.treeview_settings["Quality Procedure"] = {
	ignore_fields: ["parent_quality_procedure"],
	get_tree_nodes: "terminal_erp.quality_management.doctype.quality_procedure.quality_procedure.get_children",
	add_tree_node: "terminal_erp.quality_management.doctype.quality_procedure.quality_procedure.add_node",
	filters: [
		{
			fieldname: "parent_quality_procedure",
			fieldtype: "Link",
			options: "Quality Procedure",
			label: __("Quality Procedure"),
			get_query: function () {
				return {
					filters: [["Quality Procedure", "is_group", "=", 1]],
				};
			},
		},
	],
	breadcrumb: "Quality Management",
	disable_add_node: true,
	root_label: "All Quality Procedures",
	get_tree_root: false,
	menu_items: [
		{
			label: __("New Quality Procedure"),
			action: function () {
				terminal_framework.new_doc("Quality Procedure", true);
			},
			condition: 'terminal_framework.boot.user.can_create.indexOf("Quality Procedure") !== -1',
		},
	],
	onload: function (treeview) {
		treeview.make_tree();
	},
};
