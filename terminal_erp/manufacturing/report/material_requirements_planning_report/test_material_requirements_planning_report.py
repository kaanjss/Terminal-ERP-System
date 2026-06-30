# Copyright (c) 2024, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.manufacturing.report.material_requirements_planning_report.material_requirements_planning_report import (
	get_item_lead_time,
)
from terminal_erp.stock.doctype.item.test_item import make_item
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestMaterialRequirementsPlanningReport(Terminal ERPTestSuite):
	def test_manufacture_lead_time_is_not_int_truncated(self):
		"""lead_time = 1440 / manufacturing_time_in_mins + buffer_time. Both columns are Int;
		integer/integer division truncates on Postgres (1440/7 -> 205) while MariaDB yields a
		decimal, so the computed lead time (and the derived release date) diverged by engine."""
		item = make_item("_Test MRP Lead Time Item", {"is_stock_item": 1}).name
		terminal_framework.get_doc(
			{
				"doctype": "Item Lead Time",
				"item_code": item,
				"manufacturing_time_in_mins": 7,
				"buffer_time": 2,
			}
		).insert()

		lead_time = get_item_lead_time(item, "Manufacture")
		# 1440 / 7 + 2 = 207.714...; a truncating integer division on Postgres would give 207.
		self.assertAlmostEqual(float(lead_time), 1440 / 7 + 2, places=2)
