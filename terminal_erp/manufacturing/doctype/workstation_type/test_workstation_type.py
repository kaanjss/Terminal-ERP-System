# Copyright (c) 2022, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestWorkstationType(Terminal ERPTestSuite):
	pass


def create_workstation_type(**args):
	args = terminal_framework._dict(args)

	if workstation_type := terminal_framework.db.exists("Workstation Type", args.workstation_type):
		return terminal_framework.get_doc("Workstation Type", workstation_type)
	else:
		doc = terminal_framework.new_doc("Workstation Type")
		doc.update(args)
		doc.insert()
		return doc
