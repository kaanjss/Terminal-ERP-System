import terminal_framework


def execute():
	"""Set the payment gateway account as Email for all the existing payment channel."""
	doc_meta = terminal_framework.get_meta("Payment Gateway Account")
	if doc_meta.get_field("payment_channel"):
		return

	terminal_framework.reload_doc("Accounts", "doctype", "Payment Gateway Account")
	set_payment_channel_as_email()


def set_payment_channel_as_email():
	terminal_framework.db.sql(
		"""
		UPDATE `tabPayment Gateway Account`
		SET `payment_channel` = "Email"
	"""
	)
