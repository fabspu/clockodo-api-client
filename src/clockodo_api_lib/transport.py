from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, TypeVar
from urllib.parse import urlencode

import httpx
from pydantic import BaseModel, ValidationError

from .config import ClockodoClientConfig
from .exceptions import (
    ClockodoAPIError,
    ClockodoResponseValidationError,
    ClockodoTransportError,
)
from .pagination import CollectionResponse, Paging

T = TypeVar("T", bound=BaseModel)


def _model_to_dict(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(by_alias=True, exclude_none=True)
    if isinstance(value, Mapping):
        return {
            key: _model_to_dict(nested)
            for key, nested in value.items()
            if nested is not None
        }
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_model_to_dict(item) for item in value if item is not None]
    return value


def _flatten_payload(value: Any, prefix: str | None = None) -> list[tuple[str, Any]]:
    prepared = _model_to_dict(value)
    if prepared is None:
        return []
    if isinstance(prepared, Mapping):
        items: list[tuple[str, Any]] = []
        for key, nested in prepared.items():
            child_prefix = f"{prefix}[{key}]" if prefix else str(key)
            items.extend(_flatten_payload(nested, child_prefix))
        return items
    if isinstance(prepared, Sequence) and not isinstance(
        prepared, (str, bytes, bytearray)
    ):
        key = prefix or ""
        if prefix and "[" not in prefix:
            key = f"{prefix}[]"
        return [(key, item) for item in prepared]
    if prefix is None:
        raise ValueError("Scalar payloads require a prefix")
    return [(prefix, prepared)]


class ClockodoTransport:
    def __init__(
        self, config: ClockodoClientConfig, client: httpx.Client | None = None
    ) -> None:
        self.config = config
        self._owns_client = client is None
        self._client = client or httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout,
            headers=config.auth.headers(language=config.language),
        )

    @property
    def http_client(self) -> httpx.Client:
        return self._client

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Any | None = None,
        body: Any | None = None,
        json_mode: bool = False,
    ) -> dict[str, Any]:
        request_kwargs: dict[str, Any] = {}
        if params is not None:
            request_kwargs["params"] = _flatten_payload(params)
        if body is not None:
            if json_mode:
                request_kwargs["json"] = _model_to_dict(body)
            else:
                request_kwargs["content"] = urlencode(
                    _flatten_payload(body), doseq=True
                )
                request_kwargs["headers"] = {
                    "Content-Type": "application/x-www-form-urlencoded",
                }

        try:
            response = self._client.request(method, path, **request_kwargs)
        except httpx.HTTPError as exc:
            raise ClockodoTransportError(
                f"Clockodo transport error for {method} {path}: {exc}",
                method=method,
                path=path,
                original=exc,
            ) from exc

        payload = self._parse_json_payload(response, method=method, path=path)
        if response.status_code >= 400:
            raise ClockodoAPIError(
                f"Clockodo API request failed with status {response.status_code} for {method} {path}",
                status_code=response.status_code,
                method=method,
                path=path,
                payload=payload,
            )
        return payload

    def model(self, model_type: type[T], payload: Any, *, method: str, path: str) -> T:
        try:
            return model_type.model_validate(payload)
        except ValidationError as exc:
            raise ClockodoResponseValidationError(
                f"Could not parse Clockodo response for {method} {path}",
                method=method,
                path=path,
                payload=payload,
                errors=exc.errors(),
            ) from exc

    def optional_model(
        self, model_type: type[T], payload: Any, *, method: str, path: str
    ) -> T | None:
        if payload is None:
            return None
        return self.model(model_type, payload, method=method, path=path)

    def collection(
        self,
        model_type: type[T],
        payload: dict[str, Any],
        *,
        keys: Sequence[str],
        method: str,
        path: str,
    ) -> CollectionResponse[T]:
        raw_items: Any = None
        for key in keys:
            if key in payload:
                raw_items = payload[key]
                break
        if raw_items is None:
            raw_items = []
        if isinstance(raw_items, Mapping):
            raw_sequence = list(raw_items.values())
        else:
            raw_sequence = list(raw_items)
        items = [
            self.model(model_type, item, method=method, path=path)
            for item in raw_sequence
        ]
        paging = None
        if "paging" in payload:
            paging = self.model(Paging, payload["paging"], method=method, path=path)
        return CollectionResponse[T](items=items, paging=paging)

    def extract(self, payload: dict[str, Any], *keys: str) -> Any:
        for key in keys:
            if key in payload:
                return payload[key]
        raise KeyError(f"None of the keys {keys!r} were found in the response payload")

    def _parse_json_payload(
        self, response: httpx.Response, *, method: str, path: str
    ) -> dict[str, Any]:
        if not response.content:
            return {}
        try:
            payload = response.json()
        except ValueError as exc:
            raise ClockodoResponseValidationError(
                f"Clockodo returned a non-JSON response for {method} {path}",
                method=method,
                path=path,
                payload=response.text,
            ) from exc
        if isinstance(payload, Mapping):
            return dict(payload)
        raise ClockodoResponseValidationError(
            f"Clockodo returned an unexpected JSON shape for {method} {path}",
            method=method,
            path=path,
            payload=payload,
        )
