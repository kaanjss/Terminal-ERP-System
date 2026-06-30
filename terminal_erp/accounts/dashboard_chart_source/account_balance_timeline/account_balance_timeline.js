terminal_framework.provide("terminal_framework.dashboards.chart_sources");

terminal_framework.dashboards.chart_sources["Account Balance Timeline"] = {
	method: "terminal_erp.accounts.dashboard_chart_source.account_balance_timeline.account_balance_timeline.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: terminal_framework.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "account",
			label: __("Account"),
			fieldtype: "Link",
			options: "Account",
			reqd: 1,
			default: locals[":Company"][terminal_framework.defaults.get_user_default("Company")]["default_bank_account"],
			get_query: () => {
				return {
					filters: {
						account_type: "Bank",
						is_group: 0,
					},
				};
			},
		},
	],
};
