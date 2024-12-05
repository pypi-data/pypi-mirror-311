from typing import Optional

from syftbox.lib.exceptions import SyftBoxException


class SyftInitializationError(SyftBoxException):
    pass


class SyftBoxAlreadyRunning(SyftBoxException):
    pass


class SyftServerError(SyftBoxException):
    pass


class SyftAuthenticationError(SyftServerError):
    default_message = "Authentication failed, please log in again."

    def __init__(self, message: Optional[str] = None):
        message = self.default_message if message is None else message
        super().__init__(message)


class SyftNotFound(SyftServerError):
    pass
