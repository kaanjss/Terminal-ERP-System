# Copyright (c) 2023, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework
from terminal_framework.model.document import Document
from terminal_framework.utils import create_batch, getdate

from terminal_erp.accounts.doctype.subscription.subscription import DateTimeLikeObject


class ProcessSubscription(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		amended_from: DF.Link | None
		posting_date: DF.Date
		subscription: DF.Link | None
	# end: auto-generated types

	def on_submit(self):
		self.process_all_subscription()

	def process_all_subscription(self):
		filters = {"status": ("!=", "Cancelled")}

		if self.subscription:
			filters["name"] = self.subscription

		subscriptions = terminal_framework.get_all("Subscription", filters, pluck="name")

		for subscription in create_batch(subscriptions, 500):
			terminal_framework.enqueue(
				method="terminal_erp.accounts.doctype.subscription.subscription.process_all",
				queue="long",
				subscription=subscription,
				posting_date=self.posting_date,
			)


def create_subscription_process(
	subscription: str | None = None, posting_date: DateTimeLikeObject | None = None
):
	"""Create a new Process Subscription document"""
	doc = terminal_framework.new_doc("Process Subscription")
	doc.subscription = subscription
	doc.posting_date = getdate(posting_date)
	doc.submit()
