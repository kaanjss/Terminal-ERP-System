import terminal_framework
from terminal_framework import qb
from pypika.functions import Replace


def execute():
	sp = terminal_framework.qb.DocType("Sales Partner")
	qb.update(sp).set(sp.partner_website, Replace(sp.partner_website, "http://", "https://")).where(
		sp.partner_website.rlike("^http://.*")
	).run()
