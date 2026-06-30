import terminal_framework
from terminal_framework.model.naming import get_default_naming_series


class NamingSeriesNotSetError(terminal_framework.ValidationError):
	pass


def set_by_naming_series(doctype, fieldname, naming_series, hide_name_field=True, make_mandatory=1):
	"""Change a doctype's naming to user naming series"""
	from terminal_framework.custom.doctype.property_setter.property_setter import make_property_setter

	if naming_series:
		make_property_setter(
			doctype, "naming_series", "hidden", 0, "Check", validate_fields_for_doctype=False
		)
		make_property_setter(
			doctype, "naming_series", "reqd", make_mandatory, "Check", validate_fields_for_doctype=False
		)

		# set values for mandatory
		try:
			dt = terminal_framework.qb.DocType(doctype)
			(
				terminal_framework.qb.update(dt)
				.set(dt.naming_series, get_default_naming_series(doctype))
				.where(dt.naming_series.isnull() | (dt.naming_series == ""))
				.run()
			)
		except NamingSeriesNotSetError:
			pass

		if hide_name_field:
			make_property_setter(doctype, fieldname, "reqd", 0, "Check", validate_fields_for_doctype=False)
			make_property_setter(doctype, fieldname, "hidden", 1, "Check", validate_fields_for_doctype=False)
	else:
		make_property_setter(doctype, "naming_series", "reqd", 0, "Check", validate_fields_for_doctype=False)
		make_property_setter(
			doctype, "naming_series", "hidden", 1, "Check", validate_fields_for_doctype=False
		)

		if hide_name_field:
			make_property_setter(doctype, fieldname, "hidden", 0, "Check", validate_fields_for_doctype=False)
			make_property_setter(doctype, fieldname, "reqd", 1, "Check", validate_fields_for_doctype=False)

			# set values for mandatory
			dt = terminal_framework.qb.DocType(doctype)
			(
				terminal_framework.qb.update(dt)
				.set(dt[fieldname], dt.name)
				.where(dt[fieldname].isnull() | (dt[fieldname] == ""))
				.run()
			)
