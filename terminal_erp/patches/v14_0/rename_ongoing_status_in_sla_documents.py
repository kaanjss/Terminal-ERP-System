import terminal_framework


def execute():
	active_sla_documents = [
		sla.document_type for sla in terminal_framework.get_all("Service Level Agreement", fields=["document_type"])
	]

	for doctype in active_sla_documents:
		doctype = terminal_framework.qb.DocType(doctype)
		try:
			terminal_framework.qb.update(doctype).set(doctype.agreement_status, "First Response Due").where(
				doctype.first_responded_on.isnull()
			).run()

			terminal_framework.qb.update(doctype).set(doctype.agreement_status, "Resolution Due").where(
				doctype.agreement_status == "Ongoing"
			).run()

		except Exception:
			terminal_framework.log_error("Failed to Patch SLA Status")
