# Copyright (c) 2019, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import json

import terminal_framework
from terminal_framework import _, scrub
from terminal_framework.custom.doctype.custom_field.custom_field import create_custom_field
from terminal_framework.database.schema import validate_column_name
from terminal_framework.model import core_doctypes_list
from terminal_framework.model.document import Document
from terminal_framework.utils import cstr

from terminal_erp.accounts.doctype.repost_accounting_ledger.repost_accounting_ledger import (
	get_allowed_types_from_settings,
)


class AccountingDimension(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.accounts.doctype.accounting_dimension_detail.accounting_dimension_detail import (
			AccountingDimensionDetail,
		)

		dimension_defaults: DF.Table[AccountingDimensionDetail]
		disabled: DF.Check
		document_type: DF.Link
		fieldname: DF.Data | None
		label: DF.Data | None
	# end: auto-generated types

	def before_insert(self):
		self.set_fieldname_and_label()

	def validate(self):
		self.validate_doctype()
		validate_column_name(self.fieldname)
		self.validate_fieldname_conflict()
		self.validate_dimension_defaults()

	def validate_doctype(self):
		if self.document_type in (
			*core_doctypes_list,
			"Accounting Dimension",
			"Project",
			"Cost Center",
			"Accounting Dimension Detail",
			"Company",
			"Account",
			"Finance Book",
		):
			msg = _("Not allowed to create accounting dimension for {0}").format(self.document_type)
			terminal_framework.throw(msg)

		exists = terminal_framework.db.get_value("Accounting Dimension", {"document_type": self.document_type}, ["name"])

		if exists and self.is_new():
			terminal_framework.throw(_("Document Type already used as a dimension"))

		if not self.is_new():
			self.validate_document_type_change()

	def validate_document_type_change(self):
		doctype_before_save = terminal_framework.db.get_value("Accounting Dimension", self.name, "document_type")
		if doctype_before_save != self.document_type:
			message = _("Cannot change Reference Document Type.")
			message += _("Please create a new Accounting Dimension if required.")
			terminal_framework.throw(message)

	def validate_fieldname_conflict(self):
		conflicting_doctypes = []
		for doctype in get_doctypes_with_dimensions():
			meta = terminal_framework.get_meta(doctype, cached=False)
			if any(f.fieldname == self.fieldname for f in meta.get("fields")):
				conflicting_doctypes.append(doctype)

		if conflicting_doctypes:
			terminal_framework.msgprint(
				_(
					"Fieldname {0} already exists in the following doctypes: {1}. "
					"A separate dimension field will not be added to these doctypes. "
					"GL Entries will use the value of the existing field as the dimension value."
				).format(
					terminal_framework.bold(self.fieldname),
					", ".join(terminal_framework.bold(d) for d in conflicting_doctypes),
				),
				title=_("Fieldname Conflict"),
				indicator="orange",
			)

	def validate_dimension_defaults(self):
		companies = []
		for default in self.get("dimension_defaults"):
			if default.company not in companies:
				companies.append(default.company)
			else:
				terminal_framework.throw(_("Company {0} is added more than once").format(terminal_framework.bold(default.company)))

	def on_update(self):
		if terminal_framework.in_test:
			make_dimension_in_accounting_doctypes(doc=self)
		else:
			terminal_framework.enqueue(
				make_dimension_in_accounting_doctypes, doc=self, queue="long", enqueue_after_commit=True
			)

	def on_trash(self):
		if terminal_framework.in_test:
			delete_accounting_dimension(doc=self)
		else:
			terminal_framework.enqueue(delete_accounting_dimension, doc=self, queue="long", enqueue_after_commit=True)

	def set_fieldname_and_label(self):
		if not self.label:
			self.label = cstr(self.document_type)

		if not self.fieldname:
			self.fieldname = scrub(self.label)


def make_dimension_in_accounting_doctypes(doc, doclist=None):
	if not doclist:
		doclist = get_doctypes_with_dimensions()
	doc_count = len(get_accounting_dimensions())
	count = 0
	repostable_doctypes = get_allowed_types_from_settings(child_doc=True)

	for doctype in doclist:
		if (doc_count + 1) % 2 == 0:
			insert_after_field = "dimension_col_break"
		else:
			insert_after_field = "accounting_dimensions_section"
		df = {
			"fieldname": doc.fieldname,
			"label": doc.label,
			"fieldtype": "Link",
			"options": doc.document_type,
			"insert_after": insert_after_field,
			"owner": "Administrator",
			"allow_on_submit": 1 if doctype in repostable_doctypes else 0,
		}

		meta = terminal_framework.get_meta(doctype, cached=False)
		fieldnames = [d.fieldname for d in meta.get("fields")]

		if df["fieldname"] not in fieldnames:
			if doctype == "Budget":
				add_dimension_to_budget_doctype(df.copy(), doc)
			else:
				create_custom_field(doctype, df, ignore_validate=True)

		count += 1

		terminal_framework.publish_progress(count * 100 / len(doclist), title=_("Creating Dimensions..."))
		terminal_framework.clear_cache(doctype=doctype)


def add_dimension_to_budget_doctype(df, doc):
	df.update(
		{
			"insert_after": "cost_center",
			"depends_on": f"eval:doc.budget_against == '{doc.document_type}'",
		}
	)

	create_custom_field("Budget", df, ignore_validate=True)

	property_setter = terminal_framework.db.exists("Property Setter", "Budget-budget_against-options")

	if property_setter:
		property_setter_doc = terminal_framework.get_doc("Property Setter", "Budget-budget_against-options")
		property_setter_doc.value = property_setter_doc.value + "\n" + doc.document_type
		property_setter_doc.save()

		terminal_framework.clear_cache(doctype="Budget")
	else:
		terminal_framework.get_doc(
			{
				"doctype": "Property Setter",
				"doctype_or_field": "DocField",
				"doc_type": "Budget",
				"field_name": "budget_against",
				"property": "options",
				"property_type": "Text",
				"value": "\nCost Center\nProject\n" + doc.document_type,
			}
		).insert(ignore_permissions=True)


def delete_accounting_dimension(doc):
	doclist = get_doctypes_with_dimensions()

	terminal_framework.db.delete("Custom Field", filters={"fieldname": doc.fieldname, "dt": ["in", doclist]})

	terminal_framework.db.delete("Property Setter", filters={"field_name": doc.fieldname, "doc_type": ["in", doclist]})

	budget_against_property = terminal_framework.get_doc("Property Setter", "Budget-budget_against-options")
	value_list = budget_against_property.value.split("\n")[3:]

	if doc.document_type in value_list:
		value_list.remove(doc.document_type)

	budget_against_property.value = "\nCost Center\nProject\n" + "\n".join(value_list)
	budget_against_property.save()

	for doctype in doclist:
		terminal_framework.clear_cache(doctype=doctype)


@terminal_framework.whitelist()
def disable_dimension(doc: str):
	if terminal_framework.in_test:
		toggle_disabling(doc=doc)
	else:
		terminal_framework.enqueue(toggle_disabling, doc=doc)


def toggle_disabling(doc):
	doc = terminal_framework.parse_json(doc)

	if doc.get("disabled"):
		df = {"read_only": 1}
	else:
		df = {"read_only": 0}

	doclist = get_doctypes_with_dimensions()

	for doctype in doclist:
		field = terminal_framework.db.get_value("Custom Field", {"dt": doctype, "fieldname": doc.get("fieldname")})
		if field:
			custom_field = terminal_framework.get_doc("Custom Field", field)
			custom_field.update(df)
			custom_field.save()

		terminal_framework.clear_cache(doctype=doctype)


def get_doctypes_with_dimensions():
	return terminal_framework.get_hooks("accounting_dimension_doctypes")


def get_accounting_dimensions(as_list=True):
	accounting_dimensions = terminal_framework.get_all(
		"Accounting Dimension",
		fields=["label", "fieldname", "disabled", "document_type"],
		filters={"disabled": 0},
	)

	if as_list:
		return [d.fieldname for d in accounting_dimensions]
	else:
		return accounting_dimensions


def get_checks_for_pl_and_bs_accounts():
	AccountingDimension = terminal_framework.qb.DocType("Accounting Dimension")
	AccountingDimensionDetail = terminal_framework.qb.DocType("Accounting Dimension Detail")

	query = (
		terminal_framework.qb.from_(AccountingDimension)
		.join(AccountingDimensionDetail)
		.on(AccountingDimension.name == AccountingDimensionDetail.parent)
		.select(
			AccountingDimension.label,
			AccountingDimension.disabled,
			AccountingDimension.fieldname,
			AccountingDimensionDetail.default_dimension,
			AccountingDimensionDetail.company,
			AccountingDimensionDetail.mandatory_for_pl,
			AccountingDimensionDetail.mandatory_for_bs,
		)
		.where(AccountingDimension.disabled == 0)
	)

	return query.run(as_dict=1)


def get_dimension_with_children(doctype, dimensions):
	if isinstance(dimensions, str):
		dimensions = [dimensions]

	all_dimensions = []

	for dimension in dimensions:
		lft, rgt = terminal_framework.db.get_value(doctype, dimension, ["lft", "rgt"])
		children = terminal_framework.get_all(doctype, filters={"lft": [">=", lft], "rgt": ["<=", rgt]}, order_by="lft")
		all_dimensions += [c.name for c in children]

	return all_dimensions


@terminal_framework.whitelist()
def get_dimensions(with_cost_center_and_project: str | bool = False):
	c = terminal_framework.qb.DocType("Accounting Dimension Detail")
	p = terminal_framework.qb.DocType("Accounting Dimension")
	dimension_filters = (
		terminal_framework.qb.from_(p).select(p.label, p.fieldname, p.document_type).where(p.disabled == 0).run(as_dict=1)
	)
	default_dimensions = (
		terminal_framework.qb.from_(c)
		.inner_join(p)
		.on(c.parent == p.name)
		.select(p.fieldname, c.company, c.default_dimension)
		.run(as_dict=1)
	)

	if isinstance(with_cost_center_and_project, str):
		if with_cost_center_and_project.lower().strip() == "true":
			with_cost_center_and_project = True
		else:
			with_cost_center_and_project = False

	if with_cost_center_and_project:
		dimension_filters.extend(
			[
				terminal_framework._dict({"fieldname": "cost_center", "document_type": "Cost Center"}),
				terminal_framework._dict({"fieldname": "project", "document_type": "Project"}),
			]
		)

	default_dimensions_map = {}
	for dimension in default_dimensions:
		default_dimensions_map.setdefault(dimension.company, {})
		default_dimensions_map[dimension.company][dimension.fieldname] = dimension.default_dimension

	return dimension_filters, default_dimensions_map


def create_accounting_dimensions_for_doctype(doctype):
	accounting_dimensions = terminal_framework.db.get_all(
		"Accounting Dimension", fields=["fieldname", "label", "document_type", "disabled"]
	)

	if not accounting_dimensions:
		return

	for d in accounting_dimensions:
		field = terminal_framework.db.get_value("Custom Field", {"dt": doctype, "fieldname": d.fieldname})

		if field:
			continue

		df = {
			"fieldname": d.fieldname,
			"label": d.label,
			"fieldtype": "Link",
			"options": d.document_type,
			"insert_after": "accounting_dimensions_section",
		}

		create_custom_field(doctype, df, ignore_validate=True)

	terminal_framework.clear_cache(doctype=doctype)
