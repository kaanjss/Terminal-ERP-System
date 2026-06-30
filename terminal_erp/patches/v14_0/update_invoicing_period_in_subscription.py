import terminal_framework


def execute():
	subscription = terminal_framework.qb.DocType("Subscription")
	terminal_framework.qb.update(subscription).set(
		subscription.generate_invoice_at, "Beginning of the current subscription period"
	).where(subscription.generate_invoice_at_period_start == 1).run()
