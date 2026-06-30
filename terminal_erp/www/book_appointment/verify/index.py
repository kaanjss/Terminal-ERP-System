import terminal_framework
from terminal_framework.utils.verified_command import verify_request


def get_context(context):
	if not verify_request():
		context.success = False
		return context

	email = terminal_framework.form_dict["email"]
	appointment_name = terminal_framework.form_dict["appointment"]

	if email and appointment_name:
		appointment = terminal_framework.get_doc("Appointment", appointment_name)
		appointment.set_verified(email)
		context.success = True
		return context
	else:
		context.success = False
		return context
