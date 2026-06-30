import terminal_framework


def execute():
	try:
		item_dict = get_deferred_accounts()
		add_to_item_defaults(item_dict)
	except Exception:
		terminal_framework.db.rollback()
		terminal_framework.log_error("Failed to migrate deferred accounts in Item Defaults.")


def get_deferred_accounts():
	item = terminal_framework.qb.DocType("Item")
	return (
		terminal_framework.qb.from_(item)
		.select(item.name, item.deferred_expense_account, item.deferred_revenue_account)
		.where((item.enable_deferred_expense == 1) | (item.enable_deferred_revenue == 1))
		.run(as_dict=True)
	)


def add_to_item_defaults(item_dict):
	for item in item_dict:
		add_company_wise_item_default(item, "deferred_expense_account")
		add_company_wise_item_default(item, "deferred_revenue_account")


def add_company_wise_item_default(item, account_type):
	company = terminal_framework.get_cached_value("Account", item[account_type], "company")
	if company and item[account_type]:
		item_defaults = terminal_framework.get_cached_value("Item", item["name"], "item_defaults")
		for item_row in item_defaults:
			if item_row.company == company:
				terminal_framework.set_value("Item Default", item_row.name, account_type, item[account_type])
				break
		else:
			item_defaults.append({"company": company, account_type: item[account_type]})
			terminal_framework.set_value("Item", item["name"], "item_defaults", item_defaults)
