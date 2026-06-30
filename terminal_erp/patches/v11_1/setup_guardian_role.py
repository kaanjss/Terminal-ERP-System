import terminal_framework


def execute():
	if "Education" in terminal_framework.get_active_domains() and not terminal_framework.db.exists("Role", "Guardian"):
		doc = terminal_framework.new_doc("Role")
		doc.update({"role_name": "Guardian", "desk_access": 0})

		doc.insert(ignore_permissions=True)
