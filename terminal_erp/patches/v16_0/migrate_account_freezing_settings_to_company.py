import terminal_framework


def execute():
	rows = terminal_framework.db.sql(
		"""
		SELECT field, value
		FROM `tabSingles`
		WHERE doctype='Accounts Settings'
		AND field IN ('acc_frozen_upto', 'frozen_accounts_modifier')
		""",
		as_dict=True,
	)

	values = {row["field"]: row["value"] for row in rows}

	frozen_till = values.get("acc_frozen_upto")
	modifier = values.get("frozen_accounts_modifier")

	if not frozen_till and not modifier:
		return

	for company in terminal_framework.get_all("Company", pluck="name"):
		terminal_framework.db.set_value(
			"Company",
			company,
			{
				"accounts_frozen_till_date": frozen_till,
				"role_allowed_for_frozen_entries": modifier,
			},
		)
