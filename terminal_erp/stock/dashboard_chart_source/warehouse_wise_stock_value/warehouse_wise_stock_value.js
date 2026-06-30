terminal_framework.provide("terminal_framework.dashboards.chart_sources");

terminal_framework.dashboards.chart_sources["Warehouse wise Stock Value"] = {
	method: "terminal_erp.stock.dashboard_chart_source.warehouse_wise_stock_value.warehouse_wise_stock_value.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: terminal_framework.defaults.get_user_default("Company"),
		},
	],
};
