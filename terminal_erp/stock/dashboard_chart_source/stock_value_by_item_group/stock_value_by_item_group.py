# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from typing import Any

import terminal_framework
from terminal_framework import _
from terminal_framework.query_builder.functions import Sum
from terminal_framework.utils.dashboard import cache_source


@terminal_framework.whitelist()
@cache_source
def get(
	chart_name: str | None = None,
	chart: Any = None,
	no_cache: Any = None,
	filters: dict | str | None = None,
	from_date: Any = None,
	to_date: Any = None,
	timespan: Any = None,
	time_interval: Any = None,
	heatmap_year: Any = None,
):
	if filters and isinstance(filters, str):
		filters = terminal_framework.parse_json(filters)

	company = filters.get("company") if filters else None
	if not company:
		company = terminal_framework.defaults.get_defaults().company

	labels, datasets = get_stock_value_by_item_group(company)

	return {
		"labels": labels,
		"datasets": [{"name": _("Stock Value"), "values": datasets}],
	}


def get_stock_value_by_item_group(company):
	doctype = terminal_framework.qb.DocType("Bin")
	item_doctype = terminal_framework.qb.DocType("Item")

	warehouse_filters = [["is_group", "=", 0]]
	if company:
		warehouse_filters.append(["company", "=", company])

	warehouses = terminal_framework.get_list("Warehouse", pluck="name", filters=warehouse_filters)

	stock_value = Sum(doctype.stock_value)

	query = (
		terminal_framework.qb.from_(doctype)
		.inner_join(item_doctype)
		.on(doctype.item_code == item_doctype.name)
		.select(item_doctype.item_group, stock_value.as_("stock_value"))
		.groupby(item_doctype.item_group)
		.orderby(stock_value, order=terminal_framework.qb.desc)
		.limit(10)
	)

	if warehouses:
		query = query.where(doctype.warehouse.isin(warehouses))

	results = query.run(as_dict=True)

	labels = []
	datapoints = []

	for row in results:
		if not row.stock_value:
			continue

		labels.append(_(row.item_group))
		datapoints.append(row.stock_value)

	return labels, datapoints
