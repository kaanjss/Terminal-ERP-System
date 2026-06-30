# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework
from terminal_framework import _
from terminal_framework.utils import formatdate

from terminal_erp.controllers.website_list_for_contact import get_customers_suppliers


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = terminal_framework.get_doc(terminal_framework.form_dict.doctype, terminal_framework.form_dict.name)
	context.parents = terminal_framework.form_dict.parents
	context.doc.supplier = get_supplier()
	context.doc.rfq_links = get_link_quotation(context.doc.supplier, context.doc.name)
	unauthorized_user(context.doc.supplier)
	update_supplier_details(context)
	context["title"] = terminal_framework.form_dict.name


def get_supplier():
	doctype = terminal_framework.form_dict.doctype
	parties_doctype = "Request for Quotation Supplier" if doctype == "Request for Quotation" else doctype
	customers, suppliers = get_customers_suppliers(parties_doctype, terminal_framework.session.user)

	return suppliers[0] if suppliers else ""


def check_supplier_has_docname_access(supplier):
	status = True
	if terminal_framework.form_dict.name not in terminal_framework.get_all(
		"Request for Quotation Supplier",
		filters={"supplier": supplier},
		pluck="parent",
	):
		status = False
	return status


def unauthorized_user(supplier):
	status = check_supplier_has_docname_access(supplier) or False
	if status is False:
		terminal_framework.throw(_("Not Permitted"), terminal_framework.PermissionError)


def update_supplier_details(context):
	supplier_doc = terminal_framework.get_doc("Supplier", context.doc.supplier)
	context.doc.currency = supplier_doc.default_currency or terminal_framework.get_cached_value(
		"Company", context.doc.company, "default_currency"
	)
	context.doc.currency_symbol = terminal_framework.db.get_value("Currency", context.doc.currency, "symbol", cache=True)
	context.doc.number_format = terminal_framework.db.get_value(
		"Currency", context.doc.currency, "number_format", cache=True
	)
	context.doc.buying_price_list = supplier_doc.default_price_list or ""


def get_link_quotation(supplier, rfq):
	sqi = terminal_framework.qb.DocType("Supplier Quotation Item")
	sq = terminal_framework.qb.DocType("Supplier Quotation")
	quotation = (
		terminal_framework.qb.from_(sqi)
		.inner_join(sq)
		.on(sqi.parent == sq.name)
		.select(sqi.parent.as_("name"), sq.status, sq.transaction_date, sq.creation)
		.distinct()
		.where((sq.docstatus < 2) & (sqi.request_for_quotation == rfq) & (sq.supplier == supplier))
		.orderby(sq.creation, order=terminal_framework.qb.desc)
		.run(as_dict=1)
	)

	for data in quotation:
		data.transaction_date = formatdate(data.transaction_date)

	return quotation or None
