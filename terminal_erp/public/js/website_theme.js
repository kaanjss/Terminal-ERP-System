// Copyright (c) 2019, Terminal Framework Technologies Pvt. Ltd. and Contributors
// MIT License. See license.txt

terminal_framework.ui.form.on("Website Theme", {
	validate(frm) {
		let theme_scss = frm.doc.theme_scss;
		if (
			theme_scss &&
			theme_scss.includes("terminal_framework/public/scss/website") &&
			!theme_scss.includes("terminal_erp/public/scss/website")
		) {
			frm.set_value("theme_scss", `${frm.doc.theme_scss}\n@import "terminal_erp/public/scss/website";`);
		}
	},
});
