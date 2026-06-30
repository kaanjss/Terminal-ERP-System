import terminal_framework
from terminal_framework import _


def get_operating_cost_account(company):
	company_details = terminal_framework.db.get_value(
		"Company", company, ["default_operating_cost_account", "default_expense_account"], as_dict=True
	)

	return company_details.get("default_operating_cost_account") or company_details.get(
		"default_expense_account"
	)


def execute():
	components = [
		"Electricity",
		"Consumables",
		"Rent",
		"Wages",
	]

	companies = terminal_framework.get_all("Company", filters={"is_group": 0}, pluck="name")

	for component in components:
		component = _(component)
		if not terminal_framework.db.exists("Workstation Operating Component", component):
			doc = terminal_framework.new_doc("Workstation Operating Component")
			doc.component_name = component

			for company in companies:
				operating_cost_account = get_operating_cost_account(company)

				doc.append("accounts", {"company": company, "expense_account": operating_cost_account})

			doc.insert()

	workstations = terminal_framework.get_all("Workstation", filters={"hour_rate": (">", 0.0)}, pluck="name") or []
	workstation_types = (
		terminal_framework.get_all("Workstation Type", filters={"hour_rate": (">", 0.0)}, pluck="name") or []
	)

	if not workstations and not workstation_types:
		return

	components_map = {
		"hour_rate_electricity": _("Electricity"),
		"hour_rate_consumable": _("Consumables"),
		"hour_rate_rent": _("Rent"),
		"hour_rate_labour": _("Wages"),
	}

	for workstation in workstations:
		doc = terminal_framework.get_doc("Workstation", workstation)
		for field, component in components_map.items():
			if doc.get(field):
				doc.append(
					"workstation_costs",
					{
						"operating_component": component,
						"operating_cost": doc.get(field),
					},
				)

		doc.save()

	for workstation_type in workstation_types:
		doc = terminal_framework.get_doc("Workstation Type", workstation_type)
		for field, component in components_map.items():
			if doc.get(field):
				doc.append(
					"workstation_costs",
					{
						"operating_component": component,
						"operating_cost": doc.get(field),
					},
				)

		doc.save()
