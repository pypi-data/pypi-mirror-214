DEFAULT_STATUS_CODE = 400


def vapi_exception_handler(exception):
    return {
        "message": str(exception.message),
        "status_code": getattr(exception, "status_code", None),
        "response": getattr(exception, "response", None),
        "errors": getattr(exception, "errors", None),
    }, getattr(exception, "status_code", DEFAULT_STATUS_CODE)


class VAPIGenericError(Exception):
    def __init__(
        self, message: str, details: str = "", status_code: int = DEFAULT_STATUS_CODE
    ):
        self.message = message
        self.details = details
        self.status_code = status_code
        super().__init__(self.message)


class VAPIConfigError(VAPIGenericError):
    """Vault returned an Error"""


class VAPIVaultError(Exception):
    def __init__(self, message: str, status_code: int, errors: list = []):
        self.message = message
        self.errors = errors
        self.status_code = status_code
        super().__init__(self.message)


class VAPIPermissionDeniedError(VAPIVaultError):
    """Vault returned 403"""


class VAPIPathError(VAPIVaultError):
    """Vault returned 404"""


class VAPISealedError(VAPIVaultError):
    """Vault returned 503"""


class VAPIAcceptedStatusCodeError(VAPIVaultError):
    """The Status Code returned from Vault does match the accepted status codes set by the user"""
