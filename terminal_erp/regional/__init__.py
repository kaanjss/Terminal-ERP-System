# Copyright (c) 2018, Terminal Framework Technologies and contributors
# For license information, please see license.txt


import terminal_framework
from terminal_framework import _

from terminal_erp import get_region


def check_deletion_permission(doc, method):
	region = get_region(doc.company)
	if region in ["Nepal"] and doc.docstatus != 0:
		terminal_framework.throw(_("Deletion is not permitted for country {0}").format(region))
