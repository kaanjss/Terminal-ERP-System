from contextlib import contextmanager

import terminal_framework


@contextmanager
def temporary_flag(flag_name, value):
	flags = terminal_framework.local.flags
	flags[flag_name] = value
	try:
		yield
	finally:
		flags.pop(flag_name, None)
