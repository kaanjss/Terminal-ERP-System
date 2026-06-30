# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import terminal_framework

page_title = "Partners"


def get_context(context):
	partners = terminal_framework.get_all(
		"Sales Partner",
		filters={"show_in_website": 1},
		fields=["*"],
		order_by="name asc",
	)

	return {"partners": partners, "title": page_title}
