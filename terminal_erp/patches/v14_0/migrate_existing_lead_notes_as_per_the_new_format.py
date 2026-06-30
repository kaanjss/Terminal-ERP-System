import terminal_framework
from terminal_framework.utils import cstr, strip_html


def execute():
	for doctype in ("Lead", "Prospect", "Opportunity"):
		if not terminal_framework.db.has_column(doctype, "notes"):
			continue

		dt = terminal_framework.qb.DocType(doctype)
		records = (
			terminal_framework.qb.from_(dt).select(dt.name, dt.notes).where(dt.notes.isnotnull() & dt.notes != "")
		).run(as_dict=True)

		for d in records:
			if strip_html(cstr(d.notes)).strip():
				doc = terminal_framework.get_doc(doctype, d.name)
				doc.append("notes", {"note": d.notes})
				doc.update_child_table("notes")

		terminal_framework.db.sql_ddl(f"alter table `tab{doctype}` drop column `notes`")
