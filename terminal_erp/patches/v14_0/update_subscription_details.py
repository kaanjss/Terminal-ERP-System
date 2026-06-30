import terminal_framework


def execute():
	subscription_invoices = terminal_framework.get_all(
		"Subscription Invoice", fields=["document_type", "invoice", "parent"]
	)

	for subscription_invoice in subscription_invoices:
		terminal_framework.db.set_value(
			subscription_invoice.document_type,
			subscription_invoice.invoice,
			"subscription",
			subscription_invoice.parent,
			update_modified=False,
		)

	terminal_framework.delete_doc_if_exists("DocType", "Subscription Invoice", force=1)
