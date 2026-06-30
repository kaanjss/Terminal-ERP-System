# Copyright (c) 2022, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import terminal_framework


def execute():
	process_soa = terminal_framework.qb.DocType("Process Statement Of Accounts")
	q = terminal_framework.qb.update(process_soa).set(process_soa.report, "General Ledger")
	q.run()
