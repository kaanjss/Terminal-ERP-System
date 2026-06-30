// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.provide("terminal_erp");

// preferred modules for breadcrumbs
$.extend(terminal_framework.breadcrumbs.preferred, {
	"Item Group": "Stock",
	"Customer Group": "Selling",
	"Supplier Group": "Buying",
	Territory: "Selling",
	"Sales Person": "Selling",
	"Sales Partner": "Selling",
	Brand: "Stock",
	"Maintenance Schedule": "Support",
	"Maintenance Visit": "Support",
});

$.extend(terminal_framework.breadcrumbs.module_map, {
	"Terminal ERP Integrations": "Integrations",
	Geo: "Settings",
	Portal: "Website",
	Utilities: "Settings",
	"E-commerce": "Website",
	Contacts: "CRM",
});
