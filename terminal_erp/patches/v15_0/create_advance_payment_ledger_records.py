import terminal_framework
from terminal_framework.model.naming import _generate_random_string
from terminal_framework.query_builder import Case
from terminal_framework.utils import now_datetime

from terminal_erp.accounts.utils import get_advance_payment_doctypes

DOCTYPE = "Advance Payment Ledger Entry"

FIELDS = [
	"name",
	"creation",
	"modified",
	"owner",
	"modified_by",
	"company",
	"voucher_type",
	"voucher_no",
	"against_voucher_type",
	"against_voucher_no",
	"amount",
	"currency",
	"event",
	"delinked",
]


def execute():
	"""
	Description:
	Create Advance Payment Ledger Entry for all Payments made against Sales / Purchase Orders
	"""
	terminal_framework.db.truncate(DOCTYPE)
	advance_doctpyes = get_advance_payment_doctypes()

	if not advance_doctpyes:
		return

	make_advance_ledger_entries_for_payment_entries(advance_doctpyes)
	make_advance_ledger_entries_for_journal_entries(advance_doctpyes)


def make_advance_ledger_entries_for_payment_entries(advance_doctpyes) -> list:
	pe = terminal_framework.qb.DocType("Payment Entry")
	per = terminal_framework.qb.DocType("Payment Entry Reference")

	entries = (
		terminal_framework.qb.from_(per)
		.inner_join(pe)
		.on(pe.name == per.parent)
		.select(
			pe.company,
			per.parenttype.as_("voucher_type"),
			per.parent.as_("voucher_no"),
			per.reference_doctype.as_("against_voucher_type"),
			per.reference_name.as_("against_voucher_no"),
			per.allocated_amount.as_("amount"),
			Case()
			.when(pe.payment_type == "Receive", pe.paid_from_account_currency)
			.else_(pe.paid_to_account_currency)
			.as_("currency"),
		)
		.where(per.reference_doctype.isin(advance_doctpyes) & per.docstatus.eq(1))
		.run(as_dict=True)
	)

	if not entries:
		return

	bulk_insert_advance_entries(entries)


def make_advance_ledger_entries_for_journal_entries(advance_doctpyes) -> list:
	je = terminal_framework.qb.DocType("Journal Entry")
	jea = terminal_framework.qb.DocType("Journal Entry Account")

	entries = (
		terminal_framework.qb.from_(jea)
		.inner_join(je)
		.on(je.name == jea.parent)
		.select(
			je.company,
			jea.parenttype.as_("voucher_type"),
			jea.parent.as_("voucher_no"),
			jea.reference_type.as_("against_voucher_type"),
			jea.reference_name.as_("against_voucher_no"),
			Case()
			.when(jea.account_type == "Receivable", jea.credit_in_account_currency)
			.else_(jea.debit_in_account_currency)
			.as_("amount"),
			jea.account_currency.as_("currency"),
		)
		.where(jea.reference_type.isin(advance_doctpyes) & jea.docstatus.eq(1))
		.run(as_dict=True)
	)

	if not entries:
		return

	bulk_insert_advance_entries(entries)


def bulk_insert_advance_entries(entries):
	details = []
	user = terminal_framework.session.user
	now = now_datetime()
	for entry in entries:
		if entry.amount < 0:
			continue
		details.append(get_values(user, now, entry))

	terminal_framework.db.bulk_insert(DOCTYPE, fields=FIELDS, values=details)


def get_values(user, now, entry):
	return (
		_generate_random_string(10),
		now,
		now,
		user,
		user,
		entry.company,
		entry.voucher_type,
		entry.voucher_no,
		entry.against_voucher_type,
		entry.against_voucher_no,
		entry.amount * -1,
		entry.currency,
		"Submit",
		0,
	)
