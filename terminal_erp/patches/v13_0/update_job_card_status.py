# Copyright (c) 2021, Terminal Framework and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework


def execute():
	job_card = terminal_framework.qb.DocType("Job Card")
	(
		terminal_framework.qb.update(job_card)
		.set(job_card.status, "Completed")
		.where(
			(job_card.docstatus == 1)
			& (job_card.for_quantity <= job_card.total_completed_qty)
			& (job_card.status.isin(["Work In Progress", "Material Transferred"]))
		)
	).run()
