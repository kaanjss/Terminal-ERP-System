// Copyright (c) 2015, Terminal Framework Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

terminal_framework.provide("terminal_erp.maintenance");
terminal_framework.ui.form.on("Maintenance Schedule", {
	setup: function (frm) {
		frm.set_query("contact_person", terminal_erp.queries.contact_query);
		frm.set_query("customer_address", terminal_erp.queries.address_query);
		frm.set_query("customer", terminal_erp.queries.customer);

		frm.set_query("serial_and_batch_bundle", "items", (doc, cdt, cdn) => {
			let item = locals[cdt][cdn];

			return {
				filters: {
					item_code: item.item_code,
					voucher_type: "Maintenance Schedule",
					type_of_transaction: "Maintenance",
					company: doc.company,
				},
			};
		});
	},
	onload: function (frm) {
		if (!frm.doc.status) {
			frm.set_value({ status: "Draft" });
		}
		if (frm.doc.__islocal) {
			frm.set_value({ transaction_date: terminal_framework.datetime.get_today() });
		}
	},
	refresh: function (frm) {
		setTimeout(() => {
			frm.toggle_display("generate_schedule", !(frm.is_new() || frm.doc.docstatus));
			frm.toggle_display("schedule", !frm.is_new());
		}, 10);
	},
	customer: function (frm) {
		terminal_erp.utils.get_party_details(frm);
	},
	customer_address: function (frm) {
		terminal_erp.utils.get_address_display(frm, "customer_address", "address_display");
	},
	contact_person: function (frm) {
		terminal_erp.utils.get_contact_details(frm);
	},
	generate_schedule: function (frm) {
		if (frm.is_new()) {
			terminal_framework.msgprint(__("Please save first"));
		} else {
			frm.call("generate_schedule");
		}
	},
});

// TODO commonify this code
terminal_erp.maintenance.MaintenanceSchedule = class MaintenanceSchedule extends terminal_framework.ui.form.Controller {
	refresh() {
		terminal_framework.dynamic_link = { doc: this.frm.doc, fieldname: "customer", doctype: "Customer" };

		var me = this;

		if (this.frm.doc.docstatus === 0) {
			this.frm.add_custom_button(
				__("Sales Order"),
				function () {
					terminal_erp.utils.map_current_doc({
						method: "terminal_erp.selling.doctype.sales_order.mapper.make_maintenance_schedule",
						source_doctype: "Sales Order",
						target: me.frm,
						setters: {
							customer: me.frm.doc.customer || undefined,
						},
						get_query_filters: {
							docstatus: 1,
							company: me.frm.doc.company,
						},
					});
				},
				__("Get Items From")
			);
		} else if (this.frm.doc.docstatus === 1) {
			let schedules = me.frm.doc.schedules;
			let flag = schedules.some((schedule) => schedule.completion_status === "Pending");
			if (flag) {
				this.frm.add_custom_button(
					__("Maintenance Visit"),
					function () {
						let options = "";

						me.frm.call("get_pending_data", { data_type: "items" }).then((r) => {
							options = r.message;

							let schedule_id = "";
							let d = new terminal_framework.ui.Dialog({
								title: __("Enter Visit Details"),
								fields: [
									{
										fieldtype: "Select",
										fieldname: "item_name",
										label: __("Item Name"),
										options: options,
										reqd: 1,
										onchange: function () {
											let field = d.get_field("scheduled_date");
											me.frm
												.call("get_pending_data", {
													item_name: this.value,
													data_type: "date",
												})
												.then((r) => {
													field.df.options = r.message;
													field.refresh();
												});
										},
									},
									{
										label: __("Scheduled Date"),
										fieldname: "scheduled_date",
										fieldtype: "Select",
										options: "",
										reqd: 1,
										onchange: function () {
											let field = d.get_field("item_name");
											me.frm
												.call("get_pending_data", {
													item_name: field.value,
													s_date: this.value,
													data_type: "id",
												})
												.then((r) => {
													schedule_id = r.message;
												});
										},
									},
								],
								primary_action_label: "Create Visit",
								primary_action(values) {
									terminal_framework.call({
										method: "terminal_erp.maintenance.doctype.maintenance_schedule.maintenance_schedule.make_maintenance_visit",
										args: {
											item_name: values.item_name,
											s_id: schedule_id,
											source_name: me.frm.doc.name,
										},
										callback: function (r) {
											if (!r.exc) {
												terminal_framework.model.sync(r.message);
												terminal_framework.set_route("Form", r.message.doctype, r.message.name);
											}
										},
									});
									d.hide();
								},
							});
							d.show();
						});
					},
					__("Create")
				);
			}
		}
	}
};

extend_cscript(cur_frm.cscript, new terminal_erp.maintenance.MaintenanceSchedule({ frm: cur_frm }));
