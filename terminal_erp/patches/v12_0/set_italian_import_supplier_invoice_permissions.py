# Copyright (c) 2017, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework

from terminal_erp.regional.italy.setup import add_permissions


def execute():
	countries = terminal_framework.get_all("Company", fields="country")
	countries = [country["country"] for country in countries]
	if "Italy" in countries:
		add_permissions()
