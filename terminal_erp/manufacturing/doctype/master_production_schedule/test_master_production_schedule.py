# Copyright (c) 2025, Terminal Framework Technologies Pvt. Ltd. and Contributors
# See license.txt

import terminal_framework

from terminal_erp.manufacturing.doctype.master_production_schedule.master_production_schedule import (
	get_item_lead_time,
)
from terminal_erp.stock.doctype.item.test_item import make_item
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestMasterProductionSchedule(Terminal ERPTestSuite):
	def test_cumulative_lead_time_is_not_int_truncated(self):
		"""cumulative_lead_time = manufacturing_time_in_mins / 1440 + purchase_time + buffer_time.
		manufacturing_time_in_mins is an Int column; integer/integer division truncates on
		PostgreSQL (720/1440 -> 0) while MariaDB yields 0.5, changing the planned release date."""
		item = make_item("_Test MPS Lead Time Item", {"is_stock_item": 1}).name
		# idempotent across re-runs / a shared CI database
		terminal_framework.db.delete("Item Lead Time", {"item_code": item})
		terminal_framework.get_doc(
			{
				"doctype": "Item Lead Time",
				"item_code": item,
				"manufacturing_time_in_mins": 720,
				"purchase_time": 0,
				"buffer_time": 0,
			}
		).insert()
		# 720 / 1440 = 0.5; a truncating integer division on PostgreSQL would give 0.
		self.assertAlmostEqual(float(get_item_lead_time(item)), 0.5, places=2)
