import terminal_framework


def execute():
	terminal_framework.rename_doc("DocType", "Account Type", "Bank Account Type", force=True)
	terminal_framework.rename_doc("DocType", "Account Subtype", "Bank Account Subtype", force=True)
	terminal_framework.reload_doc("accounts", "doctype", "bank_account")
