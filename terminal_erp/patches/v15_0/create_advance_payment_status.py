import terminal_framework


def execute():
	"""
	Description:
	Calculate the new Advance Payment Statuse column in SO & PO
	"""

	if terminal_framework.reload_doc("selling", "doctype", "Sales Order"):
		so = terminal_framework.qb.DocType("Sales Order")
		terminal_framework.qb.update(so).set(so.advance_payment_status, "Not Requested").where(so.docstatus == 1).where(
			so.advance_paid == 0.0
		).run()

		terminal_framework.qb.update(so).set(so.advance_payment_status, "Partially Paid").where(so.docstatus == 1).where(
			so.advance_payment_status.isnull()
		).where(so.advance_paid < (so.rounded_total or so.grand_total)).run()

		terminal_framework.qb.update(so).set(so.advance_payment_status, "Fully Paid").where(so.docstatus == 1).where(
			so.advance_payment_status.isnull()
		).where(so.advance_paid == (so.rounded_total or so.grand_total)).run()

		pr = terminal_framework.qb.DocType("Payment Request")
		terminal_framework.qb.update(so).join(pr).on(so.name == pr.reference_name).set(
			so.advance_payment_status, "Requested"
		).where(so.docstatus == 1).where(pr.docstatus == 1).where(
			so.advance_payment_status == "Not Requested"
		).run()

	if terminal_framework.reload_doc("buying", "doctype", "Purchase Order"):
		po = terminal_framework.qb.DocType("Purchase Order")
		terminal_framework.qb.update(po).set(po.advance_payment_status, "Not Initiated").where(po.docstatus == 1).where(
			po.advance_paid == 0.0
		).run()

		terminal_framework.qb.update(po).set(po.advance_payment_status, "Partially Paid").where(po.docstatus == 1).where(
			po.advance_payment_status.isnull()
		).where(po.advance_paid < (po.rounded_total or po.grand_total)).run()

		terminal_framework.qb.update(po).set(po.advance_payment_status, "Fully Paid").where(po.docstatus == 1).where(
			po.advance_payment_status.isnull()
		).where(po.advance_paid == (po.rounded_total or po.grand_total)).run()

		pr = terminal_framework.qb.DocType("Payment Request")
		terminal_framework.qb.update(po).join(pr).on(po.name == pr.reference_name).set(
			po.advance_payment_status, "Initiated"
		).where(po.docstatus == 1).where(pr.docstatus == 1).where(
			po.advance_payment_status == "Not Initiated"
		).run()
