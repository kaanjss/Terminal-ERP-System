# Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors and Contributors
# See license.txt


import terminal_framework

from terminal_erp.stock.doctype.item_attribute.item_attribute import ItemAttributeIncrementError
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestItemAttribute(Terminal ERPTestSuite):
	def setUp(self):
		super().setUp()
		if terminal_framework.db.exists("Item Attribute", "_Test_Length"):
			terminal_framework.delete_doc("Item Attribute", "_Test_Length")

	def test_numeric_item_attribute(self):
		item_attribute = terminal_framework.get_doc(
			{
				"doctype": "Item Attribute",
				"attribute_name": "_Test_Length",
				"numeric_values": 1,
				"from_range": 0.0,
				"to_range": 100.0,
				"increment": 0,
			}
		)

		self.assertRaises(ItemAttributeIncrementError, item_attribute.save)

		item_attribute.increment = 0.5
		item_attribute.save()

	def test_validate_existing_items_finds_variants(self):
		# validate_exising_items() joins Item Variant Attribute to Item to find variants using this
		# attribute. Exercises the converted query builder version on both engines and asserts it
		# finds the variant (the raise only fires if the query returned the variant row).
		from terminal_erp.controllers.item_variant import InvalidItemAttributeValueError, create_variant

		terminal_framework.delete_doc_if_exists("Item", "_Test Variant Item-L", force=1)
		variant = create_variant("_Test Variant Item", {"Test Size": "Large"})
		variant.save()
		self.addCleanup(terminal_framework.delete_doc_if_exists, "Item", "_Test Variant Item-L", force=1)

		attribute = terminal_framework.get_doc("Item Attribute", "Test Size")
		attribute.item_attribute_values = []
		terminal_framework.flags.attribute_values = None

		# "Large" is no longer a permitted value, so the variant found by validate_exising_items
		# is invalid; the save must abort (and so never persists the cleared values).
		self.assertRaises(InvalidItemAttributeValueError, attribute.save)
