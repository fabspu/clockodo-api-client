from __future__ import annotations

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ClockodoAuth(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_user: str = Field(min_length=1, description="Clockodo user email")
    api_key: str = Field(min_length=1, description="Clockodo API key")
    application_name: str = Field(min_length=1)
    application_contact: str = Field(min_length=1, description="Technical contact email")

    @field_validator("api_user", "api_key", "application_name", "application_contact")
    @classmethod
    def _strip_and_validate(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped

    @property
    def external_application(self) -> str:
        return f"{self.application_name};{self.application_contact}"

    def headers(self, *, language: str | None = None) -> dict[str, str]:
        headers = {
            "X-ClockodoApiUser": self.api_user,
            "X-ClockodoApiKey": self.api_key,
            "X-Clockodo-External-Application": self.external_application,
            "Accept": "application/json",
        }
        if language:
            headers["Accept-Language"] = language
        return headers


class ClockodoClientConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    auth: ClockodoAuth
    base_url: str = "https://my.clockodo.com/api/v2"
    timeout: float = Field(default=30.0, gt=0)
    language: str | None = "en"

    @field_validator("base_url")
    @classmethod
    def _normalize_base_url(cls, value: str) -> str:
        normalized = value.rstrip("/")
        if not normalized:
            raise ValueError("base_url must not be empty")
        return normalized

    def with_base_url(self, base_url: str) -> Self:
        return self.model_copy(update={"base_url": base_url.rstrip("/")})
