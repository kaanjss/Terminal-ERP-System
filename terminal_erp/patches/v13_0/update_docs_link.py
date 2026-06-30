# Copyright (c) 2023, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import terminal_framework


def execute():
	navbar_settings = terminal_framework.get_single("Navbar Settings")
	for item in navbar_settings.help_dropdown:
		if item.is_standard and item.route == "https://terminal_erp.com/docs/user/manual":
			item.route = "https://docs.terminal_erp.com/docs/v14/user/manual/en/introduction"

	navbar_settings.save()
