# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from terminal_framework.model.document import Document


class ItemTax(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		item_tax_template: DF.Link
		maximum_net_rate: DF.Float
		minimum_net_rate: DF.Float
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		tax_category: DF.Link | None
		valid_from: DF.Date | None
	# end: auto-generated types

	pass
