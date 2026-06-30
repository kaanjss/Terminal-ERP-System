import json

import terminal_framework


def execute():
	uom_data = json.loads(
		open(terminal_framework.get_app_path("terminal_erp", "setup", "setup_wizard", "data", "uom_data.json")).read()
	)
	bulk_update_dict = {uom["uom_name"]: {"category": uom["category"]} for uom in uom_data}
	terminal_framework.db.bulk_update("UOM", bulk_update_dict)
