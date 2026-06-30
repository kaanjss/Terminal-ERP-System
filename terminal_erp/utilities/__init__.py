## temp utility

from contextlib import contextmanager

import terminal_framework
from terminal_framework import _
from terminal_framework.utils import cstr

from terminal_erp.utilities.activation import get_level


def update_doctypes():
	df = terminal_framework.qb.DocType("DocField")
	dt_table = terminal_framework.qb.DocType("DocType")
	for d in (
		terminal_framework.qb.from_(df)
		.inner_join(dt_table)
		.on(df.parent == dt_table.name)
		.select(df.parent, df.fieldname)
		.where(df.fieldname.like("%description%") & (dt_table.istable == 1))
		.run(as_dict=1)
	):
		dt = terminal_framework.get_doc("DocType", d.parent)

		for f in dt.fields:
			if f.fieldname == d.fieldname and f.fieldtype in ("Text", "Small Text"):
				f.fieldtype = "Text Editor"
				dt.save()
				break


def get_site_info(site_info):
	# called via hook
	company = terminal_framework.db.get_single_value("Global Defaults", "default_company")
	domain = None

	if not company:
		company = terminal_framework.get_all("Company", order_by="creation asc", pluck="name")
		company = company[0] if company else None

	if company:
		domain = terminal_framework.get_cached_value("Company", cstr(company), "domain")

	return {"company": company, "domain": domain, "activation": get_level(site_info)}


@contextmanager
def payment_app_import_guard():
	marketplace_link = '<a href="https://terminal_frameworkcloud.com/marketplace/apps/payments">Marketplace</a>'
	github_link = '<a href="https://github.com/terminal_framework/payments/">GitHub</a>'
	msg = _("payments app is not installed. Please install it from {0} or {1}").format(
		marketplace_link, github_link
	)
	try:
		yield
	except ImportError:
		terminal_framework.throw(msg, title=_("Missing Payments App"))
