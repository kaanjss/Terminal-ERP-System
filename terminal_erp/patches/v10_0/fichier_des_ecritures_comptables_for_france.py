# Copyright (c) 2018, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework

from terminal_erp.setup.doctype.company.company import install_country_fixtures


def execute():
	terminal_framework.reload_doc("regional", "report", "fichier_des_ecritures_comptables_[fec]")
	for d in terminal_framework.get_all("Company", filters={"country": "France"}):
		install_country_fixtures(d.name)
