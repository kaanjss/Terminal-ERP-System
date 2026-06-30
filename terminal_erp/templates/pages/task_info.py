import terminal_framework


def get_context(context):
	context.no_cache = 1

	task = terminal_framework.get_doc("Task", terminal_framework.form_dict.task)
	task.check_permission()

	context.comments = terminal_framework.get_all(
		"Comment",
		filters={"reference_doctype": "Task", "reference_name": task.name, "comment_type": "Comment"},
		fields=["content", "comment_email", "creation"],
	)

	context.doc = task
