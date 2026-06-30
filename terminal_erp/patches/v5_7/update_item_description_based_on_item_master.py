import terminal_framework


def execute():
	name = terminal_framework.db.sql(
		""" select name from `tabPatch Log` \
		where \
			patch like 'execute:terminal_framework.db.sql("update `tabProduction Order` pro set description%' """
	)
	if not name:
		terminal_framework.db.sql(
			"update `tabProduction Order` pro \
			set \
				description = (select description from tabItem where name=pro.production_item) \
			where \
				ifnull(description, '') = ''"
		)
