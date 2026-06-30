import terminal_framework
from terminal_framework.utils import add_days, getdate, today


def execute():
	if terminal_framework.db.exists("DocType", "Email Campaign"):
		email_campaign = terminal_framework.get_all("Email Campaign")
		for campaign in email_campaign:
			doc = terminal_framework.get_doc("Email Campaign", campaign["name"])
			send_after_days = []

			camp = terminal_framework.get_doc("Campaign", doc.campaign_name)
			for entry in camp.get("campaign_schedules"):
				send_after_days.append(entry.send_after_days)
			if send_after_days:
				end_date = add_days(getdate(doc.start_date), max(send_after_days))
				doc.db_set("end_date", end_date)
			today_date = getdate(today())
			if doc.start_date > today_date:
				doc.db_set("status", "Scheduled")
			elif end_date >= today_date:
				doc.db_set("status", "In Progress")
			elif end_date < today_date:
				doc.db_set("status", "Completed")
