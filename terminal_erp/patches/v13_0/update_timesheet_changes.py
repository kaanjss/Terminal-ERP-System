import terminal_framework
from terminal_framework.model.utils.rename_field import rename_field


def execute():
	terminal_framework.reload_doc("projects", "doctype", "timesheet")
	terminal_framework.reload_doc("projects", "doctype", "timesheet_detail")

	if terminal_framework.db.has_column("Timesheet Detail", "billable"):
		rename_field("Timesheet Detail", "billable", "is_billable")

	base_currency = terminal_framework.defaults.get_global_default("currency")

	terminal_framework.db.sql(
		"""UPDATE `tabTimesheet Detail`
			SET base_billing_rate = billing_rate,
			base_billing_amount = billing_amount,
			base_costing_rate = costing_rate,
			base_costing_amount = costing_amount"""
	)

	terminal_framework.db.sql(
		f"""UPDATE `tabTimesheet`
			SET currency = '{base_currency}',
			exchange_rate = 1.0,
			base_total_billable_amount = total_billable_amount,
			base_total_billed_amount = total_billed_amount,
			base_total_costing_amount = total_costing_amount"""
	)
