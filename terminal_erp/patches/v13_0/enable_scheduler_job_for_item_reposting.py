import terminal_framework


def execute():
	terminal_framework.reload_doc("core", "doctype", "scheduled_job_type")
	if terminal_framework.db.exists("Scheduled Job Type", "repost_item_valuation.repost_entries"):
		terminal_framework.db.set_value("Scheduled Job Type", "repost_item_valuation.repost_entries", "stopped", 0)
