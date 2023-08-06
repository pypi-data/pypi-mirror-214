DEFAULT_STATUS_CODE = 400


def vapi_exception_handler(exception):
    return {
        "message": str(exception.message),
        "status_code": exception.status_code,
        "response": exception.response,
        "errors": exception.errors,
    }, exception.status_code


class VAPIGenericError(Exception):
    def __init__(self, message: str, details: str = ""):
        self.message = message
        self.details = details
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
