# Copyright (c) 2018, Terminal Framework and contributors
# For license information, please see license.txt


import terminal_framework
from terminal_framework.model.document import Document


class QualityReview(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.quality_management.doctype.quality_review_objective.quality_review_objective import (
			QualityReviewObjective,
		)

		additional_information: DF.Text | None
		date: DF.Date | None
		goal: DF.Link
		procedure: DF.Link | None
		reviews: DF.Table[QualityReviewObjective]
		status: DF.Literal["Open", "Passed", "Failed"]
	# end: auto-generated types

	def validate(self):
		# fetch targets from goal
		if not self.reviews:
			for d in terminal_framework.get_doc("Quality Goal", self.goal).objectives:
				self.append("reviews", dict(objective=d.objective, target=d.target, uom=d.uom))

		self.set_status()

	def set_status(self):
		# if any child item is failed, fail the parent
		if not len(self.reviews or []) or any([d.status == "Open" for d in self.reviews]):
			self.status = "Open"
		elif any([d.status == "Failed" for d in self.reviews]):
			self.status = "Failed"
		else:
			self.status = "Passed"


def review():
	day = terminal_framework.utils.getdate().day
	weekday = terminal_framework.utils.getdate().strftime("%A")
	month = terminal_framework.utils.getdate().strftime("%B")

	for goal in terminal_framework.get_list("Quality Goal", fields=["name", "frequency", "date", "weekday"]):
		if goal.frequency == "Daily":
			create_review(goal.name)

		elif goal.frequency == "Weekly" and goal.weekday == weekday:
			create_review(goal.name)

		elif goal.frequency == "Monthly" and goal.date == str(day):
			create_review(goal.name)

		elif goal.frequency == "Quarterly" and day == 1 and get_quarter(month):
			create_review(goal.name)


def create_review(goal):
	goal = terminal_framework.get_doc("Quality Goal", goal)

	review = terminal_framework.get_doc({"doctype": "Quality Review", "goal": goal.name, "date": terminal_framework.utils.getdate()})

	review.insert(ignore_permissions=True)


def get_quarter(month):
	if month in ["January", "April", "July", "October"]:
		return True
	else:
		return False
