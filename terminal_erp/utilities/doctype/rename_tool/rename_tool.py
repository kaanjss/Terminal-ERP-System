# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import terminal_framework
from terminal_framework.model.document import Document
from terminal_framework.model.rename_doc import bulk_rename
from terminal_framework.utils.deprecations import deprecated


class RenameTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		file_to_rename: DF.Attach | None
		select_doctype: DF.Link | None
	# end: auto-generated types

	pass


@terminal_framework.whitelist()
@deprecated
def get_doctypes():
	return terminal_framework.get_all(
		"DocType", filters={"allow_rename": 1, "module": ["!=", "Core"]}, order_by="name", pluck="name"
	)


@terminal_framework.whitelist()
def upload(select_doctype: str | None = None):
	from terminal_framework.utils.csvutils import read_csv_content_from_attached_file

	if not select_doctype:
		select_doctype = terminal_framework.form_dict.select_doctype

	if not terminal_framework.has_permission(select_doctype, "write"):
		raise terminal_framework.PermissionError

	rows = read_csv_content_from_attached_file(terminal_framework.get_doc("Rename Tool", "Rename Tool"))

	# bulk rename allows only 500 rows at a time, so we created one job per 500 rows
	for i in range(0, len(rows), 500):
		terminal_framework.enqueue(
			method=bulk_rename,
			queue="long",
			doctype=select_doctype,
			rows=rows[i : i + 500],
		)
