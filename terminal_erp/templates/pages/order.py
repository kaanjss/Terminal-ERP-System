# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework
from terminal_framework import _

from terminal_erp.accounts.doctype.payment_request.payment_request import (
	ALLOWED_DOCTYPES_FOR_PAYMENT_REQUEST,
	get_amount,
)


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = terminal_framework.get_doc(terminal_framework.form_dict.doctype, terminal_framework.form_dict.name)
	if hasattr(context.doc, "set_indicator"):
		context.doc.set_indicator()

	context.parents = terminal_framework.form_dict.parents
	context.title = terminal_framework.form_dict.name
	context.payment_ref = terminal_framework.db.get_value(
		"Payment Request", {"reference_name": terminal_framework.form_dict.name}, "name"
	)

	default_print_format = terminal_framework.db.get_value(
		"Property Setter",
		dict(property="default_print_format", doc_type=terminal_framework.form_dict.doctype),
		"value",
	)
	if default_print_format:
		context.print_format = default_print_format
	else:
		context.print_format = "Standard"

	if not terminal_framework.has_website_permission(context.doc):
		terminal_framework.throw(_("Not Permitted"), terminal_framework.PermissionError)

	context.available_loyalty_points = 0.0
	if context.doc.get("customer"):
		# check for the loyalty program of the customer
		customer_loyalty_program = terminal_framework.db.get_value("Customer", context.doc.customer, "loyalty_program")

		if customer_loyalty_program:
			from terminal_erp.accounts.doctype.loyalty_program.loyalty_program import (
				get_loyalty_program_details_with_points,
			)

			loyalty_program_details = get_loyalty_program_details_with_points(
				context.doc.customer, customer_loyalty_program
			)
			context.available_loyalty_points = int(loyalty_program_details.get("loyalty_points"))

	context.show_pay_button, context.pay_amount = get_payment_details(context.doc)
	context.show_make_pi_button = False
	if context.doc.get("supplier"):
		# show Make Purchase Invoice button based on permission
		context.show_make_pi_button = terminal_framework.has_permission("Purchase Invoice", "create")


def get_attachments(dt, dn):
	return terminal_framework.get_all(
		"File",
		fields=["name", "file_name", "file_url", "is_private"],
		filters={"attached_to_name": dn, "attached_to_doctype": dt, "is_private": 0},
	)


def get_payment_details(doc):
	show_pay_button, amount = (
		(
			"payments" in terminal_framework.get_installed_apps()
			and terminal_framework.db.get_single_value("Buying Settings", "show_pay_button")
			and doc.doctype in ALLOWED_DOCTYPES_FOR_PAYMENT_REQUEST
		),
		0,
	)
	if not show_pay_button:
		return show_pay_button, amount

	amount = get_amount(doc)
	return bool(amount), amount
