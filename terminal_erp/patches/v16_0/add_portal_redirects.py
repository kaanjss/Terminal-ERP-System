import terminal_framework


def execute():
	if terminal_framework.db.exists("Portal Menu Item", {"route": "/addresses", "reference_doctype": "Address"}) and (
		doc := terminal_framework.get_doc("Portal Menu Item", {"route": "/addresses", "reference_doctype": "Address"})
	):
		doc.role = "Customer"
		doc.save()

	website_settings = terminal_framework.get_single("Website Settings")
	website_settings.append("route_redirects", {"source": "addresses", "target": "address/list"})
	website_settings.append("route_redirects", {"source": "projects", "target": "project"})
	website_settings.save()
