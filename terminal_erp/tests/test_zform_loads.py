""" smoak tests to check basic functionality calls on known form loads."""

import terminal_framework
from terminal_framework.desk.form.load import getdoc
from terminal_framework.www.printview import get_html_and_style

from terminal_erp.tests.utils import Terminal ERPTestSuite


class TestFormLoads(Terminal ERPTestSuite):
	@Terminal ERPTestSuite.change_settings("Print Settings", {"allow_print_for_cancelled": 1})
	def test_load(self):
		terminal_erp_modules = terminal_framework.get_all("Module Def", filters={"app_name": "terminal_erp"}, pluck="name")
		doctypes = terminal_framework.get_all(
			"DocType",
			{"istable": 0, "issingle": 0, "is_virtual": 0, "module": ("in", terminal_erp_modules)},
			pluck="name",
		)

		for doctype in doctypes:
			last_doc = terminal_framework.db.get_value(doctype, {}, "name", order_by="creation desc")
			if not last_doc:
				continue
			with self.subTest(msg=f"Loading {doctype} - {last_doc}", doctype=doctype, last_doc=last_doc):
				self.assertFormLoad(doctype, last_doc)
				self.assertDocPrint(doctype, last_doc)

	def assertFormLoad(self, doctype, docname):
		# reset previous response
		terminal_framework.response = terminal_framework._dict({"docs": []})
		terminal_framework.response.docinfo = None

		try:
			getdoc(doctype, docname)
		except Exception as e:
			self.fail(f"Failed to load {doctype}-{docname}: {e}")

		self.assertTrue(
			terminal_framework.response.docs, msg=f"expected document in reponse, found: {terminal_framework.response.docs}"
		)
		self.assertTrue(
			terminal_framework.response.docinfo, msg=f"expected docinfo in reponse, found: {terminal_framework.response.docinfo}"
		)

	def assertDocPrint(self, doctype, docname):
		doc = terminal_framework.get_doc(doctype, docname)
		doc.set("__onload", terminal_framework._dict())
		doc.run_method("onload")

		messages_before = terminal_framework.get_message_log()
		ret = get_html_and_style(doc=doc.as_json(), print_format="Standard", no_letterhead=1)
		messages_after = terminal_framework.get_message_log()

		if len(messages_after) > len(messages_before):
			new_messages = messages_after[len(messages_before) :]
			self.fail("Print view showing error/warnings: \n" + "\n".join(str(msg) for msg in new_messages))

		# html should exist
		self.assertTrue(bool(ret["html"]))
