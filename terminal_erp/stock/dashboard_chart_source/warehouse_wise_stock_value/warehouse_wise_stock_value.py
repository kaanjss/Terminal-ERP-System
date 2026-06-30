# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from typing import Any

import terminal_framework
from terminal_framework import _
from terminal_framework.utils.dashboard import cache_source


@terminal_framework.whitelist()
@cache_source
def get(
	chart_name: str | None = None,
	chart: Any | None = None,
	no_cache: Any | None = None,
	filters: dict | str | None = None,
	from_date: Any | None = None,
	to_date: Any | None = None,
	timespan: Any | None = None,
	time_interval: Any | None = None,
	heatmap_year: Any | None = None,
):
	labels, datapoints = [], []
	filters = terminal_framework.parse_json(filters)

	warehouse_filters = [["is_group", "=", 0]]
	if filters and filters.get("company"):
		warehouse_filters.append(["company", "=", filters.get("company")])

	warehouses = terminal_framework.get_list("Warehouse", pluck="name", filters=warehouse_filters, order_by="name")

	warehouses = terminal_framework.get_list(
		"Bin",
		fields=["warehouse", {"SUM": "stock_value", "as": "stock_value"}],
		filters={"warehouse": ["IN", warehouses], "stock_value": [">", 0]},
		group_by="warehouse",
		order_by="stock_value DESC",
		limit_page_length=10,
	)

	if not warehouses:
		return []

	for warehouse in warehouses:
		labels.append(_(warehouse.get("warehouse")))
		datapoints.append(warehouse.get("stock_value"))

	return {
		"labels": labels,
		"datasets": [{"name": _("Stock Value"), "values": datapoints}],
		"type": "bar",
	}
