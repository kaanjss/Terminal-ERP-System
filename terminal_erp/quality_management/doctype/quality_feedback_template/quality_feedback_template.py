# Copyright (c) 2019, Terminal Framework Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# import terminal_framework
from terminal_framework.model.document import Document


class QualityFeedbackTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from terminal_framework.types import DF

		from terminal_erp.quality_management.doctype.quality_feedback_template_parameter.quality_feedback_template_parameter import (
			QualityFeedbackTemplateParameter,
		)

		parameters: DF.Table[QualityFeedbackTemplateParameter]
		template: DF.Data
	# end: auto-generated types

	pass
