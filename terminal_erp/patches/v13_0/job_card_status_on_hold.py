import terminal_framework


def execute():
	job_cards = terminal_framework.get_all(
		"Job Card",
		{"status": "On Hold", "docstatus": ("!=", 0)},
		pluck="name",
	)

	for idx, job_card in enumerate(job_cards):
		try:
			doc = terminal_framework.get_doc("Job Card", job_card)
			doc.set_status()
			doc.db_set("status", doc.status, update_modified=False)
			if idx % 100 == 0:
				terminal_framework.db.commit()
		except Exception:
			continue
