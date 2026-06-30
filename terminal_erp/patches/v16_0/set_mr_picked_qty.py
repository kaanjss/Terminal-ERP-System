import terminal_framework


def execute():
	if data := terminal_framework.get_all(
		"Pick List Item",
		filters={"material_request_item": ["is", "set"], "docstatus": 1},
		fields=["material_request_item", {"SUM": "picked_qty", "as": "picked_qty"}],
		group_by="material_request_item",
	):
		data = {d.material_request_item: {"picked_qty": d.picked_qty} for d in data}
		terminal_framework.db.bulk_update("Material Request Item", data)
