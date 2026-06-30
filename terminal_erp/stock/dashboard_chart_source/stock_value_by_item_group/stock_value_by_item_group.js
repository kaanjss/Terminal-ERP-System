terminal_framework.provide("terminal_framework.dashboards.chart_sources");

terminal_framework.dashboards.chart_sources["Stock Value by Item Group"] = {
	method: "terminal_erp.stock.dashboard_chart_source.stock_value_by_item_group.stock_value_by_item_group.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: terminal_framework.defaults.get_user_default("Company"),
			reqd: 1,
		},
	],
};
