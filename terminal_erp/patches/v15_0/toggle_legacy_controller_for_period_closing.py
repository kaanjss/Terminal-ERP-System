import terminal_framework


def execute():
	"""
	Description:
	Enable Legacy controller for Period Closing Voucher
	"""
	terminal_framework.db.set_single_value("Accounts Settings", "use_legacy_controller_for_pcv", 1)
