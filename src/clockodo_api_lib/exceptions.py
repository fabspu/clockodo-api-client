from __future__ import annotations

from typing import Any


class ClockodoError(Exception):
    """Base class for all client errors."""


class ClockodoTransportError(ClockodoError):
    def __init__(
        self,
        message: str,
        *,
        method: str,
        path: str,
        original: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.method = method
        self.path = path
        self.original = original


class ClockodoAPIError(ClockodoError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        method: str,
        path: str,
        payload: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.method = method
        self.path = path
        self.payload = payload


class ClockodoResponseValidationError(ClockodoError):
    def __init__(
        self,
        message: str,
        *,
        method: str,
        path: str,
        payload: Any | None = None,
        errors: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.method = method
        self.path = path
        self.payload = payload
        self.errors = errors
