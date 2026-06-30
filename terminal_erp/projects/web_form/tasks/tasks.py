import urllib.parse

import terminal_framework


def get_context(context):
	if project := terminal_framework.form_dict.project:
		title = terminal_framework.utils.data.escape_html(project)
		route = "/projects?" + urllib.parse.urlencode({"project": project})
		context.parents = [{"title": title, "route": route}]
		context.success_url = route

	elif context.doc and (project := context.doc.get("project")):
		title = terminal_framework.utils.data.escape_html(project)
		route = "/projects?" + urllib.parse.urlencode({"project": project})
		context.parents = [{"title": title, "route": route}]
		context.success_url = route
