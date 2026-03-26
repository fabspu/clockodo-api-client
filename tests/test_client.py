from __future__ import annotations

from urllib.parse import parse_qs

import httpx
import pytest
import respx

from clockodo_api_lib import ClockodoAPIError, ClockodoClient, ClockodoResponseValidationError
from clockodo_api_lib.client import _ClockodoClientSurface
from clockodo_api_lib.inventory import ENDPOINT_INVENTORY
from clockodo_api_lib.models import (
    ChangeRequestCreateRequest,
    ChangeRequestInterval,
    CustomerCreateRequest,
    CustomerListParams,
)
from clockodo_api_lib.resources import (
    CRUDResource,
    ClockResource,
    CustomerProjectAccessResource,
    DefaultResources,
    EntryGroupsResource,
    EntryTextsResource,
    ServiceAccessResource,
    UserAccessGroup,
    AggregatesGroup,
    WorkTimesResource,
)


def build_client() -> ClockodoClient:
    return ClockodoClient(
        api_user="api-user@example.com",
        api_key="secret-key",
        application_name="clockodo-tests",
        application_contact="dev@example.com",
        base_url="https://api.example.test/api/v2",
    )


def resolve_public_path(client: ClockodoClient, path: tuple[str, ...]) -> object:
    current: object = client
    for segment in path:
        current = getattr(current, segment)
    return current


def test_endpoint_inventory_methods_are_exposed() -> None:
    client = build_client()
    try:
        for operation in ENDPOINT_INVENTORY:
            target = resolve_public_path(client, operation.public_path)
            assert callable(getattr(target, operation.method_name))
    finally:
        client.close()


def test_declared_client_surface_matches_default_resource_names() -> None:
    declared_resource_names = set(_ClockodoClientSurface.__annotations__) - {"config", "transport"}

    assert declared_resource_names == set(DefaultResources.__annotations__)


def test_client_resource_groups_have_concrete_runtime_types() -> None:
    client = build_client()
    try:
        assert isinstance(client.clock, ClockResource)
        assert isinstance(client.customers, CRUDResource)
        assert isinstance(client.entry_texts, EntryTextsResource)
        assert isinstance(client.entry_groups, EntryGroupsResource)
        assert isinstance(client.user_access, UserAccessGroup)
        assert isinstance(client.user_access.customer_projects, CustomerProjectAccessResource)
        assert isinstance(client.user_access.services, ServiceAccessResource)
        assert isinstance(client.aggregates, AggregatesGroup)
        assert isinstance(client.work_times, WorkTimesResource)
        assert callable(client.aggregates.users_me.get)
        assert callable(client.work_times.change_requests.list)
    finally:
        client.close()


@respx.mock
def test_create_customer_sends_form_encoded_request_with_clockodo_headers() -> None:
    route = respx.post("https://api.example.test/api/v2/customers").mock(
        return_value=httpx.Response(200, json={"customer": {"id": 1, "name": "Acme GmbH"}})
    )

    with build_client() as client:
        customer = client.customers.create(CustomerCreateRequest(name="Acme GmbH", number="C-100"))

    assert customer.id == 1
    request = route.calls.last.request
    parsed_body = parse_qs(request.content.decode())
    assert parsed_body["name"] == ["Acme GmbH"]
    assert parsed_body["number"] == ["C-100"]
    assert request.headers["X-ClockodoApiUser"] == "api-user@example.com"
    assert request.headers["X-ClockodoApiKey"] == "secret-key"
    assert request.headers["X-Clockodo-External-Application"] == "clockodo-tests;dev@example.com"


@respx.mock
def test_paginated_customer_list_is_parsed() -> None:
    respx.get("https://api.example.test/api/v2/customers").mock(
        return_value=httpx.Response(
            200,
            json={
                "paging": {
                    "items_per_page": 50,
                    "current_page": 2,
                    "count_pages": 3,
                    "count_items": 120,
                },
                "customers": [
                    {"id": 1, "name": "Acme GmbH"},
                    {"id": 2, "name": "Beta GmbH"},
                ],
            },
        )
    )

    with build_client() as client:
        response = client.customers.list(CustomerListParams(page=2))

    assert response.paging is not None
    assert response.paging.current_page == 2
    assert [customer.name for customer in response.items] == ["Acme GmbH", "Beta GmbH"]


@respx.mock
def test_change_request_create_uses_json_body() -> None:
    route = respx.post("https://api.example.test/api/v2/workTimes/changeRequests").mock(
        return_value=httpx.Response(
            200,
            json={
                "change_request": {
                    "id": 12,
                    "date": "2024-01-01",
                    "users_id": 5,
                    "status": 1,
                    "changes": [
                        {
                            "type": 1,
                            "time_since": "2024-01-01T08:00:00Z",
                            "time_until": "2024-01-01T09:00:00Z",
                        }
                    ],
                },
                "replaced_change_request": None,
                "approved_immediately": False,
            },
        )
    )

    with build_client() as client:
        response = client.work_times.change_requests.create(
            ChangeRequestCreateRequest(
                date="2024-01-01",
                users_id=5,
                changes=[
                    ChangeRequestInterval(
                        type=1,
                        time_since="2024-01-01T08:00:00Z",
                        time_until="2024-01-01T09:00:00Z",
                    )
                ],
            )
        )

    assert response.change_request is not None
    request = route.calls.last.request
    assert request.headers["content-type"].startswith("application/json")
    assert b'"users_id":5' in request.content


@respx.mock
def test_http_status_errors_preserve_payload() -> None:
    respx.get("https://api.example.test/api/v2/projects/99").mock(
        return_value=httpx.Response(403, json={"error": {"message": "forbidden"}})
    )

    with build_client() as client:
        with pytest.raises(ClockodoAPIError) as exc_info:
            client.projects.get(99)

    assert exc_info.value.status_code == 403
    assert exc_info.value.payload == {"error": {"message": "forbidden"}}


@respx.mock
def test_invalid_response_shapes_raise_validation_errors() -> None:
    respx.get("https://api.example.test/api/v2/customers/1").mock(
        return_value=httpx.Response(200, json={"customer": {"id": "bad-id"}})
    )

    with build_client() as client:
        with pytest.raises(ClockodoResponseValidationError):
            client.customers.get(1)
