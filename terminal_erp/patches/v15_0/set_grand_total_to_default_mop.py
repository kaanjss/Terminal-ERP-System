import terminal_framework


def execute():
	if terminal_framework.db.has_column("POS Profile", "disable_grand_total_to_default_mop"):
		POSProfile = terminal_framework.qb.DocType("POS Profile")

		terminal_framework.qb.update(POSProfile).set(POSProfile.set_grand_total_to_default_mop, 1).where(
			POSProfile.disable_grand_total_to_default_mop == 0
		).run()
