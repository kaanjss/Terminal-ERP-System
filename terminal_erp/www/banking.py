import json
import re

import terminal_framework
import terminal_framework.sessions
from terminal_framework import _
from terminal_framework.utils.jinja_globals import is_rtl

no_cache = 1

SCRIPT_TAG_PATTERN = re.compile(r"\<script[^<]*\</script\>", re.IGNORECASE)
CLOSING_SCRIPT_TAG_PATTERN = re.compile(r"</script\>", re.IGNORECASE)


def get_context(context):
	csrf_token = terminal_framework.sessions.get_csrf_token()

	context = terminal_framework._dict()
	context.boot = get_boot()
	context.csrf_token = csrf_token
	context.build_version = terminal_framework.utils.get_build_version()
	context.app_name = (
		terminal_framework.get_website_settings("app_name") or terminal_framework.get_system_settings("app_name") or "Terminal ERP"
	)

	context.layout_direction = "rtl" if is_rtl() else "ltr"
	context.lang = terminal_framework.local.lang

	return context


@terminal_framework.whitelist(methods=["POST"], allow_guest=True)
def get_context_for_dev():
	if not terminal_framework.conf.developer_mode:
		terminal_framework.throw(_("This method is only meant for developer mode"))
	return {
		"boot": json.loads(get_boot()),
		"layout_direction": "rtl" if is_rtl() else "ltr",
	}


def get_boot():
	try:
		boot = terminal_framework.sessions.get()
	except Exception as e:
		raise terminal_framework.SessionBootFailed from e

	boot_json = terminal_framework.as_json(boot, indent=None, separators=(",", ":"))
	boot_json = SCRIPT_TAG_PATTERN.sub("", boot_json)

	boot_json = CLOSING_SCRIPT_TAG_PATTERN.sub("", boot_json)
	boot_json = json.dumps(boot_json)

	return boot_json
