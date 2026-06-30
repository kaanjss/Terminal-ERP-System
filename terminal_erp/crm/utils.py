import terminal_framework
from terminal_framework.desk.notifications import notify_mentions
from terminal_framework.model.document import Document
from terminal_framework.utils import cstr, now, today
from pypika import functions


def disable_opportunity_creation_on_contact_us_disabled(doc, method):
	if doc.is_disabled:
		terminal_framework.db.set_single_value("CRM Settings", "enable_opportunity_creation_from_contact_us", 0)


def update_lead_phone_numbers(contact, method):
	if contact.phone_nos:
		contact_lead = contact.get_link_for("Lead")
		if contact_lead:
			phone = mobile_no = contact.phone_nos[0].phone

			if len(contact.phone_nos) > 1:
				# get the default phone number
				primary_phones = [
					phone_doc.phone for phone_doc in contact.phone_nos if phone_doc.is_primary_phone
				]
				if primary_phones:
					phone = primary_phones[0]

				# get the default mobile number
				primary_mobile_nos = [
					phone_doc.phone for phone_doc in contact.phone_nos if phone_doc.is_primary_mobile_no
				]
				if primary_mobile_nos:
					mobile_no = primary_mobile_nos[0]

			lead = terminal_framework.get_doc("Lead", contact_lead)
			lead.db_set("phone", phone)
			lead.db_set("mobile_no", mobile_no)


def copy_comments(doctype, docname, doc):
	comments = terminal_framework.db.get_values(
		"Comment",
		filters={"reference_doctype": doctype, "reference_name": docname, "comment_type": "Comment"},
		fieldname="*",
	)
	for comment in comments:
		comment = terminal_framework.get_doc(comment.update({"doctype": "Comment"}))
		comment.name = None
		comment.reference_doctype = doc.doctype
		comment.reference_name = doc.name
		comment.insert()


def link_communications(doctype, docname, doc):
	communication_list = get_linked_communication_list(doctype, docname)

	for communication in communication_list:
		communication_doc = terminal_framework.get_doc("Communication", communication)
		communication_doc.add_link(doc.doctype, doc.name, autosave=True)


def get_linked_communication_list(doctype, docname):
	communications = terminal_framework.get_all(
		"Communication", filters={"reference_doctype": doctype, "reference_name": docname}, pluck="name"
	)
	communication_links = terminal_framework.get_all(
		"Communication Link",
		{"link_doctype": doctype, "link_name": docname, "parent": ("not in", communications)},
		pluck="parent",
	)

	return communications + communication_links


def link_communications_with_prospect(communication, method):
	prospect = get_linked_prospect(communication.reference_doctype, communication.reference_name)

	if prospect:
		already_linked = any(
			[
				d.name
				for d in communication.get("timeline_links")
				if d.link_doctype == "Prospect" and d.link_name == prospect
			]
		)
		if not already_linked:
			row = communication.append("timeline_links")
			row.link_doctype = "Prospect"
			row.link_name = prospect
			row.db_update()


def update_modified_timestamp(communication, method):
	if communication.reference_doctype and communication.reference_name:
		if communication.sent_or_received == "Received" and terminal_framework.db.get_single_value(
			"CRM Settings", "update_timestamp_on_new_communication"
		):
			terminal_framework.db.set_value(
				dt=communication.reference_doctype,
				dn=communication.reference_name,
				field="modified",
				val=now(),
				update_modified=False,
			)


def get_linked_prospect(reference_doctype, reference_name):
	prospect = None
	if reference_doctype == "Lead":
		prospect = terminal_framework.db.get_value("Prospect Lead", {"lead": reference_name}, "parent")

	elif reference_doctype == "Opportunity":
		opportunity_from, party_name = terminal_framework.db.get_value(
			"Opportunity", reference_name, ["opportunity_from", "party_name"]
		)
		if opportunity_from == "Lead":
			prospect = terminal_framework.db.get_value("Prospect Opportunity", {"opportunity": reference_name}, "parent")
		if opportunity_from == "Prospect":
			prospect = party_name

	return prospect


def link_events_with_prospect(event, method):
	if event.event_participants:
		ref_doctype = event.event_participants[0].reference_doctype
		ref_docname = event.event_participants[0].reference_docname
		prospect = get_linked_prospect(ref_doctype, ref_docname)
		if prospect:
			event.add_participant("Prospect", prospect)
			event.save()


def link_open_tasks(ref_doctype, ref_docname, doc):
	todos = get_open_todos(ref_doctype, ref_docname)

	for todo in todos:
		todo_doc = terminal_framework.get_doc("ToDo", todo.name)
		todo_doc.reference_type = doc.doctype
		todo_doc.reference_name = doc.name
		todo_doc.save()


def link_open_events(ref_doctype, ref_docname, doc):
	events = get_open_events(ref_doctype, ref_docname)
	for event in events:
		event_doc = terminal_framework.get_doc("Event", event.name)
		event_doc.add_participant(doc.doctype, doc.name)
		event_doc.save()


@terminal_framework.whitelist()
def get_open_activities(ref_doctype: str, ref_docname: str):
	tasks = get_open_todos(ref_doctype, ref_docname)
	events = get_open_events(ref_doctype, ref_docname)
	tasks_history = get_closed_todos(ref_doctype, ref_docname)
	events_history = get_closed_events(ref_doctype, ref_docname)

	return {
		"tasks": tasks,
		"events": events,
		"tasks_history": tasks_history,
		"events_history": events_history,
	}


def get_closed_todos(ref_doctype, ref_docname):
	return get_filtered_todos(ref_doctype, ref_docname, status=("!=", "Open"))


def get_open_todos(ref_doctype, ref_docname):
	return get_filtered_todos(ref_doctype, ref_docname, status="Open")


def get_open_events(ref_doctype, ref_docname):
	return get_filtered_events(ref_doctype, ref_docname, open=True)


def get_closed_events(ref_doctype, ref_docname):
	return get_filtered_events(ref_doctype, ref_docname, open=False)


def get_filtered_todos(ref_doctype, ref_docname, status: str | tuple[str, str]):
	return terminal_framework.get_all(
		"ToDo",
		filters={"reference_type": ref_doctype, "reference_name": ref_docname, "status": status},
		fields=[
			"name",
			"description",
			"allocated_to",
			"date",
		],
	)


def get_filtered_events(ref_doctype, ref_docname, open: bool):
	event = terminal_framework.qb.DocType("Event")
	event_link = terminal_framework.qb.DocType("Event Participants")

	if open:
		event_status_filter = event.status == "Open"
	else:
		event_status_filter = event.status != "Open"

	query = (
		terminal_framework.qb.from_(event)
		.join(event_link)
		.on(event_link.parent == event.name)
		.select(
			event.name,
			event.subject,
			event.event_category,
			event.starts_on,
			event.ends_on,
			event.description,
		)
		.where(
			(event_link.reference_doctype == ref_doctype)
			& (event_link.reference_docname == ref_docname)
			& (event_status_filter)
		)
	)
	data = query.run(as_dict=True)

	return data


def open_leads_opportunities_based_on_todays_event():
	event = terminal_framework.qb.DocType("Event")
	event_link = terminal_framework.qb.DocType("Event Participants")

	query = (
		terminal_framework.qb.from_(event)
		.join(event_link)
		.on(event_link.parent == event.name)
		.select(event_link.reference_doctype, event_link.reference_docname)
		.where(
			(event_link.reference_doctype.isin(["Lead", "Opportunity"]))
			& (event.status == "Open")
			& (functions.Date(event.starts_on) == today())
		)
	)
	data = query.run(as_dict=True)

	for d in data:
		terminal_framework.db.set_value(d.reference_doctype, d.reference_docname, "status", "Open")


class CRMNote(Document):
	@terminal_framework.whitelist()
	def add_note(self, note: str):
		self.append("notes", {"note": note, "added_by": terminal_framework.session.user, "added_on": now()})
		self.save()
		notify_mentions(self.doctype, self.name, note)

	@terminal_framework.whitelist()
	def edit_note(self, note: str, row_id: str):
		for d in self.notes:
			if cstr(d.name) == row_id:
				d.note = note
				d.db_update()

	@terminal_framework.whitelist()
	def delete_note(self, row_id: str):
		for d in self.notes:
			if cstr(d.name) == row_id:
				self.remove(d)
				break
		self.save()
