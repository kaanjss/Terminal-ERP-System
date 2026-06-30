# Copyright (c) 2013, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from terminal_erp.selling.report.sales_analytics.sales_analytics import Analytics


def execute(filters=None):
	return Analytics(filters).run()
