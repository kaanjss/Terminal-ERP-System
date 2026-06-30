# Copyright (c) 2021, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework


# Patch kept for users outside India
def execute():
	if terminal_framework.db.exists("Company", {"country": "India"}):
		return

	for field in (
		"gst_section",
		"company_address",
		"company_gstin",
		"place_of_supply",
		"customer_address",
		"customer_gstin",
	):
		terminal_framework.delete_doc_if_exists("Custom Field", f"Payment Entry-{field}")
