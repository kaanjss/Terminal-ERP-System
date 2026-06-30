# Copyright (c) 2017, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework


def execute():
	terminal_framework.reload_doc("terminal_erp_integrations", "doctype", "plaid_settings")
	plaid_settings = terminal_framework.get_single("Plaid Settings")
	if plaid_settings.enabled:
		if not (terminal_framework.conf.plaid_client_id and terminal_framework.conf.plaid_env and terminal_framework.conf.plaid_secret):
			plaid_settings.enabled = 0
		else:
			plaid_settings.update(
				{
					"plaid_client_id": terminal_framework.conf.plaid_client_id,
					"plaid_env": terminal_framework.conf.plaid_env,
					"plaid_secret": terminal_framework.conf.plaid_secret,
				}
			)
		plaid_settings.flags.ignore_mandatory = True
		plaid_settings.save()
