import terminal_framework


def get_context(context):
	context.no_cache = 1

	timelog = terminal_framework.get_doc("Time Log", terminal_framework.form_dict.timelog)

	context.doc = timelog
