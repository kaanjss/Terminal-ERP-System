# Copyright (c) 2020, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from terminal_framework.model.document import Document
from terminal_framework.utils import time_diff_in_hours


class DowntimeEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		downtime: DF.Float
		from_time: DF.Datetime
		naming_series: DF.Literal["DT-"]
		operator: DF.Link
		remarks: DF.Text | None
		stop_reason: DF.Literal[
			"",
			"Excessive machine set up time",
			"Unplanned machine maintenance",
			"On-machine press checks",
			"Machine operator errors",
			"Machine malfunction",
			"Electricity down",
			"Other",
		]
		to_time: DF.Datetime
		workstation: DF.Link
	# end: auto-generated types

	def validate(self):
		if self.from_time and self.to_time:
			self.downtime = time_diff_in_hours(self.to_time, self.from_time) * 60
