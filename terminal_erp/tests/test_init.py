from terminal_erp import encode_company_abbr
from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestInit(Terminal ERPTestSuite):
	def test_encode_company_abbr(self):
		abbr = "NFECT"

		names = [
			"Warehouse Name",
			"Terminal ERP Foundation India",
			f"Gold - Member - {abbr}",
			f" - {abbr}",
			"Terminal ERP - Foundation - India",
			f"Terminal ERP Foundation India - {abbr}",
			f"No-Space-{abbr}",
			"- Warehouse",
		]

		expected_names = [
			f"Warehouse Name - {abbr}",
			f"Terminal ERP Foundation India - {abbr}",
			f"Gold - Member - {abbr}",
			f" - {abbr}",
			f"Terminal ERP - Foundation - India - {abbr}",
			f"Terminal ERP Foundation India - {abbr}",
			f"No-Space-{abbr} - {abbr}",
			f"- Warehouse - {abbr}",
		]

		for i in range(len(names)):
			enc_name = encode_company_abbr(names[i], abbr=abbr)
			self.assertTrue(
				enc_name == expected_names[i],
				f"{enc_name} is not same as {expected_names[i]}",
			)

	def test_translation_files(self):
		from terminal_framework.tests.test_translate import verify_translation_files

		verify_translation_files("terminal_erp")

	def test_patches(self):
		from terminal_framework.tests.test_patches import check_patch_files

		check_patch_files("terminal_erp")
