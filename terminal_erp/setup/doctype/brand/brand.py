# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework
from terminal_framework.model.document import Document


class Brand(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.stock.doctype.item_default.item_default import ItemDefault

		brand: DF.Data
		brand_defaults: DF.Table[ItemDefault]
		description: DF.Text | None
		image: DF.AttachImage | None
	# end: auto-generated types

	pass


def get_brand_defaults(item, company):
	item = terminal_framework.get_cached_doc("Item", item)
	if item.brand:
		brand = terminal_framework.get_cached_doc("Brand", item.brand)

		for d in brand.brand_defaults or []:
			if d.company == company:
				row = d.as_dict(no_private_properties=True)
				row.pop("name")
				return row

	return terminal_framework._dict()
