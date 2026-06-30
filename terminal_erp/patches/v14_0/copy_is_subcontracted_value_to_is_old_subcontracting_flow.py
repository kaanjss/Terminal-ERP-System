# Copyright (c) 2022, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework


def execute():
	for doctype in ["Purchase Order", "Purchase Receipt", "Purchase Invoice"]:
		tab = terminal_framework.qb.DocType(doctype).as_("tab")
		terminal_framework.qb.update(tab).set(tab.is_old_subcontracting_flow, 1).where(tab.is_subcontracted == 1).run()
