import terminal_framework


def execute():
	settings = terminal_framework.db.get_singles_dict("Selling Settings", cast=True)

	terminal_framework.reload_doc("crm", "doctype", "crm_settings")
	if settings:
		terminal_framework.db.set_single_value(
			"CRM Settings",
			{
				"campaign_naming_by": settings.campaign_naming_by,
				"close_opportunity_after_days": settings.close_opportunity_after_days,
				"default_valid_till": settings.default_valid_till,
			},
		)
