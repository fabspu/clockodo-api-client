from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Generic, TypeVar, TypedDict

from pydantic import BaseModel

from .models import (
    ChangeRequest,
    ChangeRequestCreateResponse,
    ClockDurationResponse,
    ClockRunningResponse,
    ClockStartRequest,
    ClockStopResponse,
    Customer,
    CustomerProjectAccessResponse,
    Entry,
    EntryGroup,
    EntryGroupDeleteRequest,
    EntryGroupListRequest,
    EntryGroupMutationPreview,
    EntryGroupMutationResult,
    EntryTextSearchResponse,
    LumpSumService,
    Project,
    Service,
    ServiceAccessResponse,
    SuccessResponse,
    SurchargeModel,
    Team,
    User,
    UserAggregateResponse,
    UserNonbusinessGroup,
    WorkTimeDay,
)
from .pagination import CollectionResponse
from .transport import ClockodoTransport

ModelT = TypeVar("ModelT", bound=BaseModel)


class CRUDResource(Generic[ModelT]):
    def __init__(
        self,
        transport: ClockodoTransport,
        *,
        path: str,
        singular_key: str,
        plural_keys: Sequence[str],
        model_type: type[ModelT],
        json_body: bool = False,
    ) -> None:
        self._transport = transport
        self._path = path
        self._singular_key = singular_key
        self._plural_keys = tuple(plural_keys)
        self._model_type = model_type
        self._json_body = json_body

    def list(
        self, params: BaseModel | Mapping[str, Any] | None = None
    ) -> CollectionResponse[ModelT]:
        payload = self._transport.request("GET", self._path, params=params)
        return self._transport.collection(
            self._model_type,
            payload,
            keys=self._plural_keys,
            method="GET",
            path=self._path,
        )

    def get(self, resource_id: int) -> ModelT:
        path = f"{self._path}/{resource_id}"
        payload = self._transport.request("GET", path)
        return self._transport.model(
            self._model_type,
            self._transport.extract(payload, self._singular_key),
            method="GET",
            path=path,
        )

    def create(self, request: BaseModel | Mapping[str, Any]) -> ModelT:
        payload = self._transport.request(
            "POST", self._path, body=request, json_mode=self._json_body
        )
        return self._transport.model(
            self._model_type,
            self._transport.extract(payload, self._singular_key),
            method="POST",
            path=self._path,
        )

    def update(
        self, resource_id: int, request: BaseModel | Mapping[str, Any]
    ) -> ModelT:
        path = f"{self._path}/{resource_id}"
        payload = self._transport.request(
            "PUT", path, body=request, json_mode=self._json_body
        )
        return self._transport.model(
            self._model_type,
            self._transport.extract(payload, self._singular_key),
            method="PUT",
            path=path,
        )

    def delete(self, resource_id: int) -> SuccessResponse:
        path = f"{self._path}/{resource_id}"
        payload = self._transport.request("DELETE", path)
        return self._transport.model(
            SuccessResponse, payload, method="DELETE", path=path
        )


class ClockResource:
    def __init__(self, transport: ClockodoTransport) -> None:
        self._transport = transport
        self._path = "/clock"

    def get_running(self) -> ClockRunningResponse:
        payload = self._transport.request("GET", self._path)
        return self._transport.model(
            ClockRunningResponse, payload, method="GET", path=self._path
        )

    def start(
        self, request: ClockStartRequest | Mapping[str, Any]
    ) -> ClockRunningResponse:
        payload = self._transport.request("POST", self._path, body=request)
        return self._transport.model(
            ClockRunningResponse, payload, method="POST", path=self._path
        )

    def stop(self, entry_id: int, *, users_id: int | None = None) -> ClockStopResponse:
        path = f"{self._path}/{entry_id}"
        params = {"users_id": users_id} if users_id is not None else None
        payload = self._transport.request("DELETE", path, params=params)
        return self._transport.model(
            ClockStopResponse, payload, method="DELETE", path=path
        )

    def change_duration(
        self,
        entry_id: int,
        request: BaseModel | Mapping[str, Any],
    ) -> ClockDurationResponse:
        path = f"{self._path}/{entry_id}"
        payload = self._transport.request("PUT", path, body=request)
        return self._transport.model(
            ClockDurationResponse, payload, method="PUT", path=path
        )


class EntryTextsResource:
    def __init__(self, transport: ClockodoTransport) -> None:
        self._transport = transport
        self._path = "/entriesTexts"

    def list(self, params: BaseModel | Mapping[str, Any]) -> EntryTextSearchResponse:
        payload = self._transport.request("GET", self._path, params=params)
        return self._transport.model(
            EntryTextSearchResponse, payload, method="GET", path=self._path
        )


class EntryGroupsResource:
    def __init__(self, transport: ClockodoTransport) -> None:
        self._transport = transport
        self._path = "/entrygroups"

    def list(
        self, request: EntryGroupListRequest | Mapping[str, Any]
    ) -> CollectionResponse[EntryGroup]:
        payload = self._transport.request("GET", self._path, params=request)
        return self._transport.collection(
            EntryGroup,
            payload,
            keys=("groups",),
            method="GET",
            path=self._path,
        )

    def update(
        self,
        request: BaseModel | Mapping[str, Any],
    ) -> EntryGroupMutationPreview | EntryGroupMutationResult:
        payload = self._transport.request(
            "PUT", self._path, body=request, json_mode=True
        )
        if "confirm_key" in payload:
            return self._transport.model(
                EntryGroupMutationPreview, payload, method="PUT", path=self._path
            )
        return self._transport.model(
            EntryGroupMutationResult, payload, method="PUT", path=self._path
        )

    def delete(
        self,
        request: EntryGroupDeleteRequest | Mapping[str, Any],
    ) -> EntryGroupMutationPreview | EntryGroupMutationResult:
        payload = self._transport.request(
            "DELETE", self._path, body=request, json_mode=True
        )
        if "confirm_key" in payload:
            return self._transport.model(
                EntryGroupMutationPreview, payload, method="DELETE", path=self._path
            )
        return self._transport.model(
            EntryGroupMutationResult, payload, method="DELETE", path=self._path
        )


class CustomerProjectAccessResource:
    def __init__(self, transport: ClockodoTransport) -> None:
        self._transport = transport

    def get(self, user_id: int) -> CustomerProjectAccessResponse:
        path = f"/users/{user_id}/access/customers-projects"
        payload = self._transport.request("GET", path)
        return self._transport.model(
            CustomerProjectAccessResponse, payload, method="GET", path=path
        )


class ServiceAccessResource:
    def __init__(self, transport: ClockodoTransport) -> None:
        self._transport = transport

    def get(self, user_id: int) -> ServiceAccessResponse:
        path = f"/users/{user_id}/access/services"
        payload = self._transport.request("GET", path)
        return self._transport.model(
            ServiceAccessResponse, payload, method="GET", path=path
        )


class UserAccessGroup:
    def __init__(self, transport: ClockodoTransport) -> None:
        self.customer_projects = CustomerProjectAccessResource(transport)
        self.services = ServiceAccessResource(transport)


class AggregatesUsersMeResource:
    def __init__(self, transport: ClockodoTransport) -> None:
        self._transport = transport
        self._path = "/aggregates/users/me"

    def get(self) -> UserAggregateResponse:
        payload = self._transport.request("GET", self._path)
        return self._transport.model(
            UserAggregateResponse, payload, method="GET", path=self._path
        )


class AggregatesGroup:
    def __init__(self, transport: ClockodoTransport) -> None:
        self.users_me = AggregatesUsersMeResource(transport)


class WorkTimeChangeRequestsResource:
    def __init__(self, transport: ClockodoTransport) -> None:
        self._transport = transport
        self._path = "/workTimes/changeRequests"

    def list(
        self, params: BaseModel | Mapping[str, Any] | None = None
    ) -> CollectionResponse[ChangeRequest]:
        payload = self._transport.request("GET", self._path, params=params)
        return self._transport.collection(
            ChangeRequest,
            payload,
            keys=("change_requests",),
            method="GET",
            path=self._path,
        )

    def create(
        self, request: BaseModel | Mapping[str, Any]
    ) -> ChangeRequestCreateResponse:
        payload = self._transport.request(
            "POST", self._path, body=request, json_mode=True
        )
        return self._transport.model(
            ChangeRequestCreateResponse, payload, method="POST", path=self._path
        )

    def approve(self, resource_id: int) -> ChangeRequest | None:
        path = f"{self._path}/{resource_id}/approve"
        payload = self._transport.request("POST", path)
        return self._transport.optional_model(
            ChangeRequest,
            payload.get("change_request"),
            method="POST",
            path=path,
        )

    def decline(self, resource_id: int) -> ChangeRequest | None:
        path = f"{self._path}/{resource_id}/decline"
        payload = self._transport.request("POST", path)
        return self._transport.optional_model(
            ChangeRequest,
            payload.get("change_request"),
            method="POST",
            path=path,
        )

    def delete(self, resource_id: int) -> ChangeRequest | None:
        path = f"{self._path}/{resource_id}"
        payload = self._transport.request("DELETE", path)
        return self._transport.optional_model(
            ChangeRequest,
            payload.get("change_request"),
            method="DELETE",
            path=path,
        )


class WorkTimesResource:
    def __init__(self, transport: ClockodoTransport) -> None:
        self._transport = transport
        self._path = "/workTimes"
        self.change_requests = WorkTimeChangeRequestsResource(transport)

    def list(
        self, params: BaseModel | Mapping[str, Any]
    ) -> CollectionResponse[WorkTimeDay]:
        payload = self._transport.request("GET", self._path, params=params)
        return self._transport.collection(
            WorkTimeDay,
            payload,
            keys=("work_time_days",),
            method="GET",
            path=self._path,
        )


class DefaultResources(TypedDict):
    clock: ClockResource
    customers: CRUDResource[Customer]
    entries: CRUDResource[Entry]
    entry_texts: EntryTextsResource
    entry_groups: EntryGroupsResource
    lump_sum_services: CRUDResource[LumpSumService]
    projects: CRUDResource[Project]
    services: CRUDResource[Service]
    surcharges: CRUDResource[SurchargeModel]
    teams: CRUDResource[Team]
    users: CRUDResource[User]
    users_nonbusiness_groups: CRUDResource[UserNonbusinessGroup]
    user_access: UserAccessGroup
    aggregates: AggregatesGroup
    work_times: WorkTimesResource


def build_default_resources(transport: ClockodoTransport) -> DefaultResources:
    return {
        "clock": ClockResource(transport),
        "customers": CRUDResource[Customer](
            transport,
            path="/customers",
            singular_key="customer",
            plural_keys=("customers",),
            model_type=Customer,
        ),
        "entries": CRUDResource[Entry](
            transport,
            path="/entries",
            singular_key="entry",
            plural_keys=("entries",),
            model_type=Entry,
        ),
        "entry_texts": EntryTextsResource(transport),
        "entry_groups": EntryGroupsResource(transport),
        "lump_sum_services": CRUDResource[LumpSumService](
            transport,
            path="/lumpsumservices",
            singular_key="lumpSumService",
            plural_keys=("lumpSumServices",),
            model_type=LumpSumService,
        ),
        "projects": CRUDResource[Project](
            transport,
            path="/projects",
            singular_key="project",
            plural_keys=("projects",),
            model_type=Project,
        ),
        "services": CRUDResource[Service](
            transport,
            path="/services",
            singular_key="service",
            plural_keys=("services",),
            model_type=Service,
        ),
        "surcharges": CRUDResource[SurchargeModel](
            transport,
            path="/surcharges",
            singular_key="surcharge",
            plural_keys=("surcharges",),
            model_type=SurchargeModel,
            json_body=True,
        ),
        "teams": CRUDResource[Team](
            transport,
            path="/teams",
            singular_key="team",
            plural_keys=("teams", "team"),
            model_type=Team,
        ),
        "users": CRUDResource[User](
            transport,
            path="/users",
            singular_key="user",
            plural_keys=("users",),
            model_type=User,
        ),
        "users_nonbusiness_groups": CRUDResource[UserNonbusinessGroup](
            transport,
            path="/usersNonbusinessGroups",
            singular_key="data",
            plural_keys=("data",),
            model_type=UserNonbusinessGroup,
        ),
        "user_access": UserAccessGroup(transport),
        "aggregates": AggregatesGroup(transport),
        "work_times": WorkTimesResource(transport),
    }
