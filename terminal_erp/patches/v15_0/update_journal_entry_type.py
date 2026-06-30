import terminal_framework


def execute():
	custom_je_type = terminal_framework.db.get_value(
		"Property Setter",
		{"doc_type": "Journal Entry", "field_name": "voucher_type", "property": "options"},
		["name", "value"],
		as_dict=True,
	)
	if custom_je_type:
		custom_je_type.value += "\nAsset Disposal"
		terminal_framework.db.set_value("Property Setter", custom_je_type.name, "value", custom_je_type.value)

	scrapped_journal_entries = terminal_framework.get_all(
		"Asset", filters={"journal_entry_for_scrap": ["is", "not set"]}, fields=["name"]
	)
	for je in scrapped_journal_entries:
		terminal_framework.db.set_value("Journal Entry", je.name, "voucher_type", "Asset Disposal")
