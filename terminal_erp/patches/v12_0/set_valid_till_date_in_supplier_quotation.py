import terminal_framework


def execute():
	terminal_framework.reload_doc("buying", "doctype", "supplier_quotation")
	terminal_framework.db.sql(
		"""UPDATE `tabSupplier Quotation`
		SET valid_till = DATE_ADD(transaction_date , INTERVAL 1 MONTH)
		WHERE docstatus < 2"""
	)
