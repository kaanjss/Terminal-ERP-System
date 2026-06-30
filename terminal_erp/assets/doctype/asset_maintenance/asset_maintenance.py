# Copyright (c) 2017, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from typing import Any

import terminal_framework
from terminal_framework import _, throw
from terminal_framework.desk.form import assign_to
from terminal_framework.model.document import Document
from terminal_framework.utils import DateTimeLikeObject, add_days, add_months, add_years, getdate, nowdate


class AssetMaintenance(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.assets.doctype.asset_maintenance_task.asset_maintenance_task import AssetMaintenanceTask

		asset_category: DF.ReadOnly | None
		asset_maintenance_tasks: DF.Table[AssetMaintenanceTask]
		asset_name: DF.Link
		company: DF.Link
		item_code: DF.ReadOnly | None
		item_name: DF.ReadOnly | None
		maintenance_manager: DF.Data | None
		maintenance_manager_name: DF.ReadOnly | None
		maintenance_team: DF.Link
	# end: auto-generated types

	def validate(self):
		for task in self.get("asset_maintenance_tasks"):
			if task.end_date and (getdate(task.start_date) >= getdate(task.end_date)):
				throw(_("Start date should be less than end date for task {0}").format(task.maintenance_task))
			if getdate(task.next_due_date) < getdate(nowdate()):
				task.maintenance_status = "Overdue"
			if not task.assign_to and self.docstatus == 0:
				throw(_("Row #{}: Please assign task to a member.").format(task.idx))

	def on_update(self):
		for task in self.get("asset_maintenance_tasks"):
			assign_tasks(self.name, task.assign_to, task.maintenance_task, task.next_due_date)
		self.sync_maintenance_tasks()

	def after_delete(self):
		asset = terminal_framework.get_doc("Asset", self.asset_name)
		if asset.status == "In Maintenance":
			asset.set_status()

	def sync_maintenance_tasks(self):
		tasks_names = []
		for task in self.get("asset_maintenance_tasks"):
			tasks_names.append(task.name)
			update_maintenance_log(
				asset_maintenance=self.name, item_code=self.item_code, item_name=self.item_name, task=task
			)
		asset_maintenance_logs = terminal_framework.get_all(
			"Asset Maintenance Log",
			fields=["name"],
			filters={"asset_maintenance": self.name, "task": ("not in", tasks_names)},
		)
		if asset_maintenance_logs:
			for asset_maintenance_log in asset_maintenance_logs:
				maintenance_log = terminal_framework.get_doc("Asset Maintenance Log", asset_maintenance_log.name)
				maintenance_log.db_set("maintenance_status", "Cancelled")


def assign_tasks(asset_maintenance_name, assign_to_member, maintenance_task, next_due_date):
	team_member = terminal_framework.db.get_value("User", assign_to_member, "email")
	args = {
		"doctype": "Asset Maintenance",
		"assign_to": team_member,
		"name": asset_maintenance_name,
		"description": maintenance_task,
		"date": next_due_date,
	}
	if not terminal_framework.db.exists(
		"ToDo",
		{
			"reference_type": args["doctype"],
			"reference_name": args["name"],
			"status": "Open",
			"owner": args["assign_to"],
		},
	):
		# assign_to function expects a list
		args["assign_to"] = [args["assign_to"]]
		assign_to.add(args)


@terminal_framework.whitelist()
def calculate_next_due_date(
	periodicity: str,
	start_date: DateTimeLikeObject | None = None,
	end_date: DateTimeLikeObject | None = None,
	last_completion_date: DateTimeLikeObject | None = None,
	next_due_date: DateTimeLikeObject | None = None,
):
	if not start_date and not last_completion_date:
		start_date = terminal_framework.utils.now()

	if last_completion_date and ((start_date and last_completion_date > start_date) or not start_date):
		start_date = last_completion_date
	if periodicity == "Daily":
		next_due_date = add_days(start_date, 1)
	if periodicity == "Weekly":
		next_due_date = add_days(start_date, 7)
	if periodicity == "Monthly":
		next_due_date = add_months(start_date, 1)
	if periodicity == "Quarterly":
		next_due_date = add_months(start_date, 3)
	if periodicity == "Half-yearly":
		next_due_date = add_months(start_date, 6)
	if periodicity == "Yearly":
		next_due_date = add_years(start_date, 1)
	if periodicity == "2 Yearly":
		next_due_date = add_years(start_date, 2)
	if periodicity == "3 Yearly":
		next_due_date = add_years(start_date, 3)
	if end_date and (
		(start_date and start_date >= end_date)
		or (last_completion_date and last_completion_date >= end_date)
		or next_due_date
	):
		next_due_date = ""
	return next_due_date


def update_maintenance_log(asset_maintenance, item_code, item_name, task):
	asset_maintenance_log = terminal_framework.get_value(
		"Asset Maintenance Log",
		{
			"asset_maintenance": asset_maintenance,
			"task": task.name,
			"maintenance_status": ("in", ["Planned", "Overdue"]),
		},
	)

	if not asset_maintenance_log:
		asset_maintenance_log = terminal_framework.get_doc(
			{
				"doctype": "Asset Maintenance Log",
				"asset_maintenance": asset_maintenance,
				"asset_name": asset_maintenance,
				"item_code": item_code,
				"item_name": item_name,
				"task": task.name,
				"has_certificate": task.certificate_required,
				"description": task.description,
				"assign_to_name": task.assign_to_name,
				"task_assignee_email": task.assign_to,
				"periodicity": str(task.periodicity),
				"maintenance_type": task.maintenance_type,
				"due_date": task.next_due_date,
			}
		)
		asset_maintenance_log.insert()
	else:
		maintenance_log = terminal_framework.get_doc("Asset Maintenance Log", asset_maintenance_log)
		maintenance_log.assign_to_name = task.assign_to_name
		maintenance_log.has_certificate = task.certificate_required
		maintenance_log.description = task.description
		maintenance_log.periodicity = str(task.periodicity)
		maintenance_log.maintenance_type = task.maintenance_type
		maintenance_log.due_date = task.next_due_date
		maintenance_log.save()


@terminal_framework.whitelist()
@terminal_framework.validate_and_sanitize_search_inputs
def get_team_members(
	doctype: str,
	txt: str,
	searchfield: str,
	start: int,
	page_len: int,
	filters: dict[str, Any],
) -> list[tuple[str]]:
	return terminal_framework.db.get_values(
		"Maintenance Team Member",
		{"parent": filters.get("maintenance_team")},
		"team_member",
	)


@terminal_framework.whitelist()
def get_maintenance_log(asset_name: str):
	return terminal_framework.get_all(
		"Asset Maintenance Log",
		filters={"asset_name": asset_name},
		fields=["maintenance_status", {"COUNT": "asset_name", "as": "count"}, "asset_name"],
		group_by="maintenance_status, asset_name",
	)
