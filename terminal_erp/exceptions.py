import terminal_framework


# accounts
class PartyFrozen(terminal_framework.ValidationError):
	pass


class InvalidAccountCurrency(terminal_framework.ValidationError):
	pass


class InvalidCurrency(terminal_framework.ValidationError):
	pass


class PartyDisabled(terminal_framework.ValidationError):
	pass


class InvalidAccountDimensionError(terminal_framework.ValidationError):
	pass


class MandatoryAccountDimensionError(terminal_framework.ValidationError):
	pass


class ReportingCurrencyExchangeNotFoundError(terminal_framework.ValidationError):
	pass


# stock
class QualityInspectionRequiredError(terminal_framework.ValidationError):
	pass


class QualityInspectionRejectedError(terminal_framework.ValidationError):
	pass


class QualityInspectionNotSubmittedError(terminal_framework.ValidationError):
	pass


class BatchExpiredError(terminal_framework.ValidationError):
	pass
