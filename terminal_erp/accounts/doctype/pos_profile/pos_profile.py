# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework
from terminal_framework import _, msgprint
from terminal_framework.core.doctype.user_permission.user_permission import get_permitted_documents
from terminal_framework.model.document import Document
from terminal_framework.utils import get_link_to_form, now

from terminal_erp.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_checks_for_pl_and_bs_accounts,
)


class POSProfile(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.accounts.doctype.pos_customer_group.pos_customer_group import POSCustomerGroup
		from terminal_erp.accounts.doctype.pos_item_group.pos_item_group import POSItemGroup
		from terminal_erp.accounts.doctype.pos_payment_method.pos_payment_method import POSPaymentMethod
		from terminal_erp.accounts.doctype.pos_profile_user.pos_profile_user import POSProfileUser

		account_for_change_amount: DF.Link | None
		action_on_new_invoice: DF.Literal[
			"Always Ask", "Save Changes and Load New Invoice", "Discard Changes and Load New Invoice"
		]
		allow_discount_change: DF.Check
		allow_partial_payment: DF.Check
		allow_rate_change: DF.Check
		allow_warehouse_change: DF.Check
		applicable_for_users: DF.Table[POSProfileUser]
		apply_discount_on: DF.Literal["Grand Total", "Net Total"]
		auto_add_item_to_cart: DF.Check
		company: DF.Link
		company_address: DF.Link | None
		cost_center: DF.Link | None
		country: DF.ReadOnly | None
		currency: DF.Link
		customer: DF.Link | None
		customer_groups: DF.Table[POSCustomerGroup]
		disable_rounded_total: DF.Check
		disabled: DF.Check
		expense_account: DF.Link | None
		hide_images: DF.Check
		hide_unavailable_items: DF.Check
		ignore_pricing_rule: DF.Check
		income_account: DF.Link | None
		item_groups: DF.Table[POSItemGroup]
		letter_head: DF.Link | None
		payments: DF.Table[POSPaymentMethod]
		print_format: DF.Link | None
		print_receipt_on_order_complete: DF.Check
		project: DF.Link | None
		select_print_heading: DF.Link | None
		selling_price_list: DF.Link | None
		set_grand_total_to_default_mop: DF.Check
		tax_category: DF.Link | None
		taxes_and_charges: DF.Link | None
		tc_name: DF.Link | None
		update_stock: DF.Check
		utm_campaign: DF.Link | None
		utm_medium: DF.Link | None
		utm_source: DF.Link | None
		validate_stock_on_save: DF.Check
		warehouse: DF.Link
		write_off_account: DF.Link
		write_off_cost_center: DF.Link
		write_off_limit: DF.Currency
	# end: auto-generated types

	def validate(self):
		self.validate_disabled()
		self.validate_default_profile()
		self.validate_all_link_fields()
		self.validate_duplicate_groups()
		self.validate_payment_methods()
		self.validate_accounting_dimensions()

	def validate_accounting_dimensions(self):
		acc_dims = get_checks_for_pl_and_bs_accounts()
		for acc_dim in acc_dims:
			if (
				self.company == acc_dim.company
				and not self.get(acc_dim.fieldname)
				and (acc_dim.mandatory_for_pl or acc_dim.mandatory_for_bs)
			):
				terminal_framework.throw(
					_(
						"{0} is a mandatory Accounting Dimension. <br>"
						"Please set a value for {0} in Accounting Dimensions section."
					).format(
						terminal_framework.bold(acc_dim.label),
					),
					title=_("Mandatory Accounting Dimension"),
				)

	def validate_disabled(self):
		old_doc = self.get_doc_before_save()

		if (
			old_doc
			and self.disabled
			and old_doc.disabled != self.disabled
			and terminal_framework.db.exists("POS Opening Entry", {"pos_profile": self.name, "status": "Open"})
		):
			terminal_framework.throw(
				_("POS Profile {0} cannot be disabled as there are ongoing POS sessions.").format(
					terminal_framework.bold(self.name)
				)
			)

	def validate_default_profile(self):
		for row in self.applicable_for_users:
			pfu = terminal_framework.qb.DocType("POS Profile User")
			pf = terminal_framework.qb.DocType("POS Profile")
			res = (
				terminal_framework.qb.from_(pfu)
				.inner_join(pf)
				.on(pf.name == pfu.parent)
				.select(pf.name)
				.where(
					(pfu.user == row.user)
					& (pf.name != self.name)
					& (pf.company == self.company)
					& (pfu.default == 1)
					& (pf.disabled == 0)
				)
				.run()
			)

			if row.default and res:
				msgprint(
					_("Already set default in pos profile {0} for user {1}, kindly disabled default").format(
						res[0][0], row.user
					),
					raise_exception=1,
				)
			elif not row.default and not res:
				msgprint(
					_(
						"User {0} doesn't have any default POS Profile. Check Default at Row {1} for this User."
					).format(row.user, row.idx)
				)

	def validate_all_link_fields(self):
		accounts = {
			"Account": [self.income_account, self.expense_account],
			"Cost Center": [self.cost_center],
			"Warehouse": [self.warehouse],
		}

		for link_dt, dn_list in accounts.items():
			for link_dn in dn_list:
				if link_dn and not terminal_framework.db.exists(
					{"doctype": link_dt, "company": self.company, "name": link_dn}
				):
					terminal_framework.throw(_("{0} does not belong to Company {1}").format(link_dn, self.company))

	def validate_duplicate_groups(self):
		item_groups = [d.item_group for d in self.item_groups]
		customer_groups = [d.customer_group for d in self.customer_groups]

		if len(item_groups) != len(set(item_groups)):
			terminal_framework.throw(
				_("Duplicate item group found in the item group table"), title=_("Duplicate Item Group")
			)

		if len(customer_groups) != len(set(customer_groups)):
			terminal_framework.throw(
				_("Duplicate customer group found in the customer group table"),
				title=_("Duplicate Customer Group"),
			)

	def validate_payment_methods(self):
		if not self.payments:
			terminal_framework.throw(_("Payment methods are mandatory. Please add at least one payment method."))

		default_mode = [d.default for d in self.payments if d.default]
		if not default_mode:
			terminal_framework.throw(_("Please select a default mode of payment"))

		if len(default_mode) > 1:
			terminal_framework.throw(_("You can only select one mode of payment as default"))

		invalid_modes = []
		for d in self.payments:
			account = terminal_framework.db.get_value(
				"Mode of Payment Account",
				{"parent": d.mode_of_payment, "company": self.company},
				"default_account",
			)

			if not account:
				invalid_modes.append(get_link_to_form("Mode of Payment", d.mode_of_payment))

		if invalid_modes:
			if invalid_modes == 1:
				msg = _("Please set default Cash or Bank account in Mode of Payment {0}")
			else:
				msg = _("Please set default Cash or Bank account in Mode of Payments {0}")
			terminal_framework.throw(msg.format(", ".join(invalid_modes)), title=_("Missing Account"))

	def on_update(self):
		self.set_defaults()

	def on_trash(self):
		self.set_defaults(include_current_pos=False)

	def set_defaults(self, include_current_pos=True):
		terminal_framework.defaults.clear_default("is_pos")

		pfu = terminal_framework.qb.DocType("POS Profile User")

		query = terminal_framework.qb.from_(pfu).select(pfu.user).where(pfu.default == 1)

		if not include_current_pos:
			query = query.where(pfu.name != self.name)

		pos_view_users = query.run(as_list=1, pluck=True)

		for user in pos_view_users:
			if user:
				terminal_framework.defaults.set_user_default("is_pos", 1, user)
			else:
				terminal_framework.defaults.set_global_default("is_pos", 1)


def get_item_groups(pos_profile):
	item_groups = []
	pos_profile = terminal_framework.get_cached_doc("POS Profile", pos_profile)
	permitted_item_groups = get_permitted_nodes("Item Group")

	if pos_profile.get("item_groups"):
		# Get items based on the item groups defined in the POS profile
		for data in pos_profile.get("item_groups"):
			item_groups.extend(
				[
					d.name
					for d in get_child_nodes("Item Group", data.item_group)
					if not permitted_item_groups or d.name in permitted_item_groups
				]
			)

	if not item_groups and permitted_item_groups:
		item_groups = list(permitted_item_groups)

	# Return raw Item Group names; the callers parameterize them via the query builder
	# (item_group.isin(...)) / terminal_framework.get_all, which escapes them once. Pre-escaping here would
	# double-escape (item_group IN ('''X''')) and match nothing.
	return list(set(item_groups))


def get_permitted_nodes(group_type):
	nodes = []
	permitted_nodes = get_permitted_documents(group_type)

	if not permitted_nodes:
		return nodes

	for node in permitted_nodes:
		if terminal_framework.db.get_value(group_type, node, "is_group"):
			nodes.extend([d.name for d in get_child_nodes(group_type, node)])
		else:
			nodes.append(node)

	return nodes


def get_child_nodes(group_type, root):
	lft, rgt = terminal_framework.db.get_value(group_type, root, ["lft", "rgt"])
	return terminal_framework.get_all(
		group_type,
		filters={"lft": [">=", lft], "rgt": ["<=", rgt]},
		fields=["name", "lft", "rgt"],
		order_by="lft",
	)


@terminal_framework.whitelist()
@terminal_framework.validate_and_sanitize_search_inputs
def pos_profile_query(doctype: str, txt: str, searchfield: str, start: int, page_len: int, filters: dict):
	user = terminal_framework.session["user"]
	company = filters.get("company") or terminal_framework.defaults.get_user_default("company")

	pf = terminal_framework.qb.DocType("POS Profile")
	pfu = terminal_framework.qb.DocType("POS Profile User")

	pos_profile = (
		terminal_framework.qb.from_(pf)
		.inner_join(pfu)
		.on(pfu.parent == pf.name)
		.select(pf.name)
		.where((pfu.user == user) & (pf.company == company) & pf.name.like(f"%{txt}%") & (pf.disabled == 0))
		.limit(page_len)
		.offset(start)
		.run()
	)

	if not pos_profile:
		pos_profile = (
			terminal_framework.qb.from_(pf)
			.left_join(pfu)
			.on(pf.name == pfu.parent)
			.select(pf.name)
			.where(
				(pfu.user.isnull() | (pfu.user == ""))
				& (pf.company == company)
				& pf.name.like(f"%{txt}%")
				& (pf.disabled == 0)
			)
			.run()
		)

	return pos_profile
