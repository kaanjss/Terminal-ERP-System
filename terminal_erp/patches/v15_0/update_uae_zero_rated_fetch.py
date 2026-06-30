import terminal_framework

from terminal_erp.regional.united_arab_emirates.setup import make_custom_fields


def execute():
	if not terminal_framework.db.get_value("Company", {"country": "United Arab Emirates"}):
		return

	make_custom_fields()
