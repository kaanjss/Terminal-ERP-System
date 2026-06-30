// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Workstation", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(1);

	terminal_framework.run_serially("Workstation", [
		// insert a new Workstation
		() =>
			terminal_framework.tests.make([
				// values to be set
				{ key: "value" },
			]),
		() => {
			assert.equal(cur_frm.doc.key, "value");
		},
		() => done(),
	]);
});
