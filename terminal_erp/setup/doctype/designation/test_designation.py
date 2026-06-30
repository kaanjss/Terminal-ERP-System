# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import terminal_framework


def create_designation(**args):
	args = terminal_framework._dict(args)
	if terminal_framework.db.exists("Designation", args.designation_name or "_Test designation"):
		return terminal_framework.get_doc("Designation", args.designation_name or "_Test designation")

	designation = terminal_framework.get_doc(
		{
			"doctype": "Designation",
			"designation_name": args.designation_name or "_Test designation",
			"description": args.description or "_Test description",
		}
	)
	designation.save()
	return designation
