if (!window.terminal_framework) window.terminal_framework = {};

terminal_framework.provide = function (namespace) {
	// docs: create a namespace //
	var nsl = namespace.split(".");
	var parent = window;
	for (var i = 0; i < nsl.length; i++) {
		var n = nsl[i];
		if (!parent[n]) {
			parent[n] = {};
		}
		parent = parent[n];
	}
	return parent;
};

terminal_framework.provide("locals");
terminal_framework.provide("terminal_framework.flags");
terminal_framework.provide("terminal_framework.settings");
terminal_framework.provide("locals.DocType");
terminal_framework.provide("terminal_framework.model");
terminal_framework.provide("terminal_framework.defaults");
