// Copyright (c) 2018, Terminal Framework Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

terminal_framework.provide("terminal_erp.integrations");

terminal_framework.ui.form.on("Plaid Settings", {
	enabled: function (frm) {
		frm.toggle_reqd("plaid_client_id", frm.doc.enabled);
		frm.toggle_reqd("plaid_secret", frm.doc.enabled);
		frm.toggle_reqd("plaid_env", frm.doc.enabled);
	},

	refresh: function (frm) {
		if (frm.doc.enabled) {
			frm.add_custom_button(__("Link a new bank account"), () => {
				new terminal_erp.integrations.plaidLink(frm);
			});

			frm.add_custom_button(__("Reset Plaid Link"), () => {
				new terminal_erp.integrations.plaidLink(frm);
			});

			frm.add_custom_button(__("Sync Now"), () => {
				terminal_framework.call({
					method: "terminal_erp.terminal_erp_integrations.doctype.plaid_settings.plaid_settings.enqueue_synchronization",
					freeze: true,
					callback: () => {
						let bank_transaction_link = terminal_framework.utils.get_form_link(
							"Bank Transaction",
							"",
							true,
							__("Bank Transaction")
						);

						terminal_framework.msgprint({
							title: __("Sync Started"),
							message: __(
								"The sync has started in the background, please check the {0} list for new records.",
								[bank_transaction_link]
							),
							alert: 1,
						});
					},
				});
			}).addClass("btn-primary");
		}
	},
});

terminal_erp.integrations.plaidLink = class plaidLink {
	constructor(parent) {
		this.frm = parent;
		this.plaidUrl = "https://cdn.plaid.com/link/v2/stable/link-initialize.js";
		this.init_config();
	}

	async init_config() {
		this.product = ["transactions"];
		this.plaid_env = this.frm.doc.plaid_env;
		this.client_name = terminal_framework.boot.sitename;
		this.token = await this.get_link_token();
		this.init_plaid();
	}

	async get_link_token() {
		const token = await this.frm.call("get_link_token").then((resp) => resp.message);
		if (!token) {
			terminal_framework.throw(__("Cannot retrieve link token. Check Error Log for more information"));
		}
		return token;
	}

	init_plaid() {
		const me = this;
		me.loadScript(me.plaidUrl)
			.then(() => {
				me.onScriptLoaded(me);
			})
			.then(() => {
				if (me.linkHandler) {
					me.linkHandler.open();
				}
			})
			.catch((error) => {
				me.onScriptError(error);
			});
	}

	loadScript(src) {
		return new Promise(function (resolve, reject) {
			if (document.querySelector('script[src="' + src + '"]')) {
				resolve();
				return;
			}
			const el = document.createElement("script");
			el.type = "text/javascript";
			el.async = true;
			el.src = src;
			el.addEventListener("load", resolve);
			el.addEventListener("error", reject);
			el.addEventListener("abort", reject);
			document.head.appendChild(el);
		});
	}

	onScriptLoaded(me) {
		me.linkHandler = Plaid.create({
			// eslint-disable-line no-undef
			clientName: me.client_name,
			product: me.product,
			env: me.plaid_env,
			token: me.token,
			onSuccess: me.plaid_success,
		});
	}

	onScriptError(error) {
		terminal_framework.msgprint(
			__(
				"There was an issue connecting to Plaid's authentication server. Check browser console for more information"
			)
		);
		console.log(error);
	}

	plaid_success(token, response) {
		const me = this;

		terminal_framework.prompt(
			{
				fieldtype: "Link",
				options: "Company",
				label: __("Company"),
				fieldname: "company",
				reqd: 1,
			},
			(data) => {
				me.company = data.company;
				terminal_framework
					.xcall(
						"terminal_erp.terminal_erp_integrations.doctype.plaid_settings.plaid_settings.add_institution",
						{
							token: token,
							response: response,
						}
					)
					.then((result) => {
						terminal_framework.xcall(
							"terminal_erp.terminal_erp_integrations.doctype.plaid_settings.plaid_settings.add_bank_accounts",
							{
								response: response,
								bank: result,
								company: me.company,
							}
						);
					})
					.then(() => {
						terminal_framework.show_alert({ message: __("Bank accounts added"), indicator: "green" });
					});
			},
			__("Select a company"),
			__("Continue")
		);
	}
};
