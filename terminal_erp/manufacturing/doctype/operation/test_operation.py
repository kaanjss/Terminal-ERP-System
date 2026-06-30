# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestOperation(Terminal ERPTestSuite):
	pass


def make_operation(*args, **kwargs):
	args = args if args else kwargs
	if isinstance(args, tuple):
		args = args[0]

	args = terminal_framework._dict(args)

	if not terminal_framework.db.exists("Operation", args.operation):
		doc = terminal_framework.get_doc(
			{"doctype": "Operation", "name": args.operation, "workstation": args.workstation}
		)
		doc.insert()
		return doc

	return terminal_framework.get_doc("Operation", args.operation)
