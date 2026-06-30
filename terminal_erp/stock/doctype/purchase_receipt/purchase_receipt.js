// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.provide("terminal_erp.stock");

cur_frm.cscript.tax_table = "Purchase Taxes and Charges";

terminal_erp.accounts.taxes.setup_tax_filters("Purchase Taxes and Charges");
terminal_erp.accounts.taxes.setup_tax_validations("Purchase Receipt");
terminal_erp.buying.setup_buying_controller();

terminal_framework.ui.form.on("Purchase Receipt", {
	setup: (frm) => {
		frm.custom_make_buttons = {
			"Stock Entry": "Return",
			"Purchase Invoice": "Purchase Invoice",
			"Landed Cost Voucher": "Landed Cost Voucher",
		};

		frm.set_query("wip_composite_asset", "items", function () {
			return {
				filters: { asset_type: "Composite Asset", docstatus: 0 },
			};
		});

		frm.set_query("taxes_and_charges", function () {
			return {
				filters: { company: frm.doc.company },
			};
		});
	},
	onload: function (frm) {
		terminal_erp.queries.setup_queries(frm, "Warehouse", function () {
			return terminal_erp.queries.warehouse(frm.doc);
		});
	},

	refresh: function (frm) {
		if (frm.doc.company) {
			frm.trigger("toggle_display_account_head");
		}

		if (frm.doc.docstatus === 1 && frm.doc.is_return === 1 && frm.doc.per_billed !== 100) {
			frm.add_custom_button(
				__("Debit Note"),
				function () {
					terminal_framework.model.open_mapped_doc({
						method: "terminal_erp.stock.doctype.purchase_receipt.mapper.make_purchase_invoice",
						frm: cur_frm,
					});
				},
				__("Create")
			);
			frm.page.set_inner_btn_group_as_primary(__("Create"));
		}

		if (frm.doc.docstatus === 1 && frm.doc.is_internal_supplier && !frm.doc.inter_company_reference) {
			frm.add_custom_button(
				__("Delivery Note"),
				function () {
					terminal_framework.model.open_mapped_doc({
						method: "terminal_erp.stock.doctype.purchase_receipt.mapper.make_inter_company_delivery_note",
						frm: cur_frm,
					});
				},
				__("Create")
			);
		}

		if (frm.doc.docstatus === 0) {
			if (!frm.doc.is_return) {
				terminal_framework.db.get_single_value("Buying Settings", "maintain_same_rate").then((value) => {
					if (value) {
						frm.doc.items.forEach((item) => {
							frm.fields_dict.items.grid.update_docfield_property(
								"rate",
								"read_only",
								item.purchase_order && item.purchase_order_item
							);
						});
					}
				});
			}
		}

		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(
				__("Landed Cost Voucher"),
				() => {
					frm.events.make_lcv(frm);
				},
				__("Create")
			);
		}

		frm.events.add_custom_buttons(frm);
	},

	make_lcv(frm) {
		terminal_framework.call({
			method: "terminal_erp.stock.doctype.purchase_receipt.purchase_receipt.make_lcv",
			args: {
				doctype: frm.doc.doctype,
				docname: frm.doc.name,
			},
			callback: (r) => {
				if (r.message) {
					var doc = terminal_framework.model.sync(r.message);
					terminal_framework.set_route("Form", doc[0].doctype, doc[0].name);
				}
			},
		});
	},

	add_custom_buttons: function (frm) {
		if (frm.doc.docstatus == 0) {
			frm.add_custom_button(
				__("Purchase Invoice"),
				function () {
					if (!frm.doc.supplier) {
						terminal_framework.throw({
							title: __("Mandatory"),
							message: __("Please Select a Supplier"),
						});
					}
					terminal_erp.utils.map_current_doc({
						method: "terminal_erp.accounts.doctype.purchase_invoice.mapper.make_purchase_receipt",
						source_doctype: "Purchase Invoice",
						target: frm,
						setters: {
							supplier: frm.doc.supplier,
						},
						get_query_filters: {
							docstatus: 1,
							per_received: ["<", 100],
							company: frm.doc.company,
							update_stock: 0,
						},
						allow_child_item_selection: true,
						child_fieldname: "items",
						child_columns: ["item_code", "item_name", "qty", "received_qty"],
					});
				},
				__("Get Items From")
			);
		}
	},

	company: function (frm) {
		frm.trigger("toggle_display_account_head");
		terminal_erp.accounts.dimensions.update_dimension(frm, frm.doctype);
	},

	toggle_display_account_head: function (frm) {
		var enabled = terminal_erp.is_perpetual_inventory_enabled(frm.doc.company);
		frm.fields_dict["items"].grid.set_column_disp(["cost_center"], enabled);
	},
});

terminal_erp.stock.PurchaseReceiptController = class PurchaseReceiptController extends (
	terminal_erp.buying.BuyingController
) {
	setup(doc) {
		this.setup_accounting_dimension_triggers();
		this.setup_posting_date_time_check();
		super.setup(doc);

		this.frm.set_query("expense_account", "items", () => {
			return {
				query: "terminal_erp.controllers.queries.get_expense_account",
				filters: {
					company: this.frm.doc.company,
					disabled: 0,
				},
			};
		});
	}

	refresh() {
		var me = this;
		super.refresh();

		terminal_erp.accounts.ledger_preview.show_accounting_ledger_preview(this.frm);
		terminal_erp.accounts.ledger_preview.show_stock_ledger_preview(this.frm);

		if (this.frm.doc.docstatus > 0) {
			this.show_stock_ledger();
			//removed for temporary
			this.show_general_ledger();

			this.frm.add_custom_button(
				__("Asset"),
				function () {
					terminal_framework.route_options = {
						purchase_receipt: me.frm.doc.name,
					};
					terminal_framework.set_route("List", "Asset");
				},
				__("View")
			);

			this.frm.add_custom_button(
				__("Asset Movement"),
				function () {
					terminal_framework.route_options = {
						reference_name: me.frm.doc.name,
					};
					terminal_framework.set_route("List", "Asset Movement");
				},
				__("View")
			);
		}

		if (!this.frm.doc.is_return && this.frm.doc.status != "Closed") {
			if (this.frm.doc.docstatus == 0) {
				this.frm.add_custom_button(
					__("Purchase Order"),
					function () {
						if (!me.frm.doc.supplier) {
							terminal_framework.throw({
								title: __("Mandatory"),
								message: __("Please Select a Supplier"),
							});
						}
						terminal_erp.utils.map_current_doc({
							method: "terminal_erp.buying.doctype.purchase_order.mapper.make_purchase_receipt",
							source_doctype: "Purchase Order",
							target: me.frm,
							setters: {
								supplier: me.frm.doc.supplier,
								schedule_date: undefined,
							},
							get_query_filters: {
								docstatus: 1,
								status: ["not in", ["Closed", "On Hold"]],
								per_received: ["<", 99.99],
								company: me.frm.doc.company,
							},
							allow_child_item_selection: true,
							child_fieldname: "items",
							child_columns: ["item_code", "item_name", "qty", "received_qty"],
						});
					},
					__("Get Items From")
				);
			}

			if (this.frm.doc.docstatus == 1 && this.frm.doc.status != "Closed") {
				if (this.frm.has_perm("submit")) {
					cur_frm.add_custom_button(__("Close"), this.close_purchase_receipt, __("Status"));
				}

				cur_frm.add_custom_button(__("Purchase Return"), this.make_purchase_return, __("Create"));

				cur_frm.add_custom_button(
					__("Make Stock Entry"),
					cur_frm.cscript["Make Stock Entry"],
					__("Create")
				);

				if (flt(this.frm.doc.per_billed) < 100) {
					cur_frm.add_custom_button(
						__("Purchase Invoice"),
						this.make_purchase_invoice,
						__("Create")
					);
				}
				cur_frm.add_custom_button(
					__("Sample Retention Stock Entry"),
					this.make_retention_stock_entry,
					__("Create")
				);

				cur_frm.page.set_inner_btn_group_as_primary(__("Create"));
			}
		}

		if (this.frm.doc.docstatus == 1 && this.frm.doc.status === "Closed" && this.frm.has_perm("submit")) {
			cur_frm.add_custom_button(__("Reopen"), this.reopen_purchase_receipt, __("Status"));
		}
	}

	make_purchase_invoice() {
		terminal_framework.model.open_mapped_doc({
			method: "terminal_erp.stock.doctype.purchase_receipt.mapper.make_purchase_invoice",
			frm: cur_frm,
		});
	}

	make_purchase_return() {
		let me = this;

		let has_rejected_items = cur_frm.doc.items.filter((item) => {
			if (item.rejected_qty > 0) {
				return true;
			}
		});

		if (has_rejected_items && has_rejected_items.length > 0) {
			terminal_framework.prompt(
				[
					{
						label: __("Return Qty from Rejected Warehouse"),
						fieldtype: "Check",
						fieldname: "return_for_rejected_warehouse",
						default: 1,
					},
				],
				function (values) {
					if (values.return_for_rejected_warehouse) {
						terminal_framework.call({
							method: "terminal_erp.stock.doctype.purchase_receipt.mapper.make_purchase_return_against_rejected_warehouse",
							args: {
								source_name: cur_frm.doc.name,
							},
							callback: function (r) {
								if (r.message) {
									terminal_framework.model.sync(r.message);
									terminal_framework.set_route("Form", r.message.doctype, r.message.name);
								}
							},
						});
					} else {
						cur_frm.cscript._make_purchase_return();
					}
				},
				__("Return Qty"),
				__("Make Return Entry")
			);
		} else {
			cur_frm.cscript._make_purchase_return();
		}
	}

	close_purchase_receipt() {
		cur_frm.cscript.update_status("Closed");
	}

	reopen_purchase_receipt() {
		cur_frm.cscript.update_status("Submitted");
	}

	make_retention_stock_entry() {
		terminal_framework.call({
			method: "terminal_erp.stock.doctype.stock_entry.stock_entry_handler.manufacturing.move_sample_to_retention_warehouse",
			args: {
				company: cur_frm.doc.company,
				items: cur_frm.doc.items,
			},
			callback: function (r) {
				if (r.message) {
					var doc = terminal_framework.model.sync(r.message)[0];
					terminal_framework.set_route("Form", doc.doctype, doc.name);
				} else {
					terminal_framework.msgprint(
						__("Purchase Receipt does not have any Item for which Retain Sample is enabled.")
					);
				}
			},
		});
	}

	apply_putaway_rule() {
		if (this.frm.doc.apply_putaway_rule) terminal_erp.apply_putaway_rule(this.frm);
	}

	items_add(doc, cdt, cdn) {
		const row = terminal_framework.get_doc(cdt, cdn);
		const field_copy = ["expense_account", "cost_center"];
		if (doc.project) {
			terminal_framework.model.set_value(cdt, cdn, "project", doc.project);
		} else {
			field_copy.push("project");
		}
		this.frm.script_manager.copy_from_first_row("items", row, field_copy);
	}
};

// for backward compatibility: combine new and previous states
extend_cscript(cur_frm.cscript, new terminal_erp.stock.PurchaseReceiptController({ frm: cur_frm }));

cur_frm.cscript.update_status = function (status) {
	terminal_framework.ui.form.is_saving = true;
	terminal_framework.call({
		method: "terminal_erp.stock.doctype.purchase_receipt.purchase_receipt.update_purchase_receipt_status",
		args: { docname: cur_frm.doc.name, status: status },
		callback: function (r) {
			if (!r.exc) cur_frm.reload_doc();
		},
		always: function () {
			terminal_framework.ui.form.is_saving = false;
		},
	});
};

cur_frm.fields_dict["items"].grid.get_field("project").get_query = function (doc, cdt, cdn) {
	return {
		filters: [["Project", "status", "not in", "Completed, Cancelled"]],
	};
};

cur_frm.fields_dict["select_print_heading"].get_query = function (doc, cdt, cdn) {
	return {
		filters: [["Print Heading", "docstatus", "!=", "2"]],
	};
};

cur_frm.fields_dict["items"].grid.get_field("bom").get_query = function (doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return {
		filters: [
			["BOM", "item", "=", d.item_code],
			["BOM", "is_active", "=", "1"],
			["BOM", "docstatus", "=", "1"],
		],
	};
};

terminal_framework.provide("terminal_erp.buying");

terminal_framework.ui.form.on("Purchase Receipt Item", {
	item_code: function (frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		terminal_framework.db.get_value("Item", { name: d.item_code }, "sample_quantity", (r) => {
			terminal_framework.model.set_value(cdt, cdn, "sample_quantity", r.sample_quantity);
			validate_sample_quantity(frm, cdt, cdn);
		});
	},
	qty: function (frm, cdt, cdn) {
		validate_sample_quantity(frm, cdt, cdn);
	},
	sample_quantity: function (frm, cdt, cdn) {
		validate_sample_quantity(frm, cdt, cdn);
	},
	batch_no: function (frm, cdt, cdn) {
		validate_sample_quantity(frm, cdt, cdn);
	},
});

cur_frm.cscript._make_purchase_return = function () {
	terminal_framework.model.open_mapped_doc({
		method: "terminal_erp.stock.doctype.purchase_receipt.mapper.make_purchase_return",
		frm: cur_frm,
	});
};

cur_frm.cscript["Make Stock Entry"] = function () {
	terminal_framework.model.open_mapped_doc({
		method: "terminal_erp.stock.doctype.purchase_receipt.mapper.make_stock_entry",
		frm: cur_frm,
	});
};

var validate_sample_quantity = function (frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.sample_quantity && d.qty) {
		terminal_framework.call({
			method: "terminal_erp.stock.doctype.stock_entry.stock_entry_handler.manufacturing.validate_sample_quantity",
			args: {
				batch_no: d.batch_no,
				item_code: d.item_code,
				sample_quantity: d.sample_quantity,
				qty: d.qty,
			},
			callback: (r) => {
				terminal_framework.model.set_value(cdt, cdn, "sample_quantity", r.message);
			},
		});
	}
};
