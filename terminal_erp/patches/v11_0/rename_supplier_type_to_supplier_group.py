import terminal_framework
from terminal_framework import _
from terminal_framework.model.utils.rename_field import rename_field
from terminal_framework.utils.nestedset import rebuild_tree


def execute():
	if terminal_framework.db.table_exists("Supplier Group"):
		terminal_framework.reload_doc("setup", "doctype", "supplier_group")
	elif terminal_framework.db.table_exists("Supplier Type"):
		terminal_framework.rename_doc("DocType", "Supplier Type", "Supplier Group", force=True)
		terminal_framework.reload_doc("setup", "doctype", "supplier_group")
		terminal_framework.reload_doc("accounts", "doctype", "pricing_rule")
		terminal_framework.reload_doc("accounts", "doctype", "tax_rule")
		terminal_framework.reload_doc("buying", "doctype", "buying_settings")
		terminal_framework.reload_doc("buying", "doctype", "supplier")
		rename_field("Supplier Group", "supplier_type", "supplier_group_name")
		rename_field("Supplier", "supplier_type", "supplier_group")
		rename_field("Buying Settings", "supplier_type", "supplier_group")
		rename_field("Pricing Rule", "supplier_type", "supplier_group")
		rename_field("Tax Rule", "supplier_type", "supplier_group")

	build_tree()


def build_tree():
	terminal_framework.db.sql(
		"""update `tabSupplier Group` set parent_supplier_group = '{}'
		where is_group = 0""".format(_("All Supplier Groups"))
	)

	if not terminal_framework.db.exists("Supplier Group", _("All Supplier Groups")):
		terminal_framework.get_doc(
			{
				"doctype": "Supplier Group",
				"supplier_group_name": _("All Supplier Groups"),
				"is_group": 1,
				"parent_supplier_group": "",
			}
		).insert(ignore_permissions=True)

	rebuild_tree("Supplier Group")
