# Copyright (c) 2023, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import terminal_framework
from terminal_framework.model.document import Document
from terminal_framework.utils import now_datetime


class AssetActivity(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		asset: DF.Link
		date: DF.Datetime
		subject: DF.SmallText
		user: DF.Link
	# end: auto-generated types

	pass


def add_asset_activity(asset, subject):
	terminal_framework.get_doc(
		{
			"doctype": "Asset Activity",
			"asset": asset,
			"subject": subject,
			"user": terminal_framework.session.user,
			"date": now_datetime(),
		}
	).insert(ignore_permissions=True, ignore_links=True)
