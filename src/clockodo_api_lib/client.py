from __future__ import annotations

from typing import Any

import httpx

from .config import ClockodoAuth, ClockodoClientConfig
from .inventory import ENDPOINT_INVENTORY
from .models import (
    Customer,
    Entry,
    LumpSumService,
    Project,
    Service,
    SurchargeModel,
    Team,
    User,
    UserNonbusinessGroup,
)
from .resources import (
    AggregatesGroup,
    CRUDResource,
    ClockResource,
    DefaultResources,
    EntryGroupsResource,
    EntryTextsResource,
    UserAccessGroup,
    WorkTimesResource,
    build_default_resources,
)
from .transport import ClockodoTransport


class _ClockodoClientSurface:
    config: ClockodoClientConfig
    transport: ClockodoTransport
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


class ClockodoClient(_ClockodoClientSurface):
    def __init__(
        self,
        *,
        api_user: str,
        api_key: str,
        application_name: str,
        application_contact: str,
        base_url: str = "https://my.clockodo.com/api/v2",
        timeout: float = 30.0,
        language: str | None = "en",
        http_client: httpx.Client | None = None,
    ) -> None:
        self.config = ClockodoClientConfig(
            auth=ClockodoAuth(
                api_user=api_user,
                api_key=api_key,
                application_name=application_name,
                application_contact=application_contact,
            ),
            base_url=base_url,
            timeout=timeout,
            language=language,
        )
        self.transport = ClockodoTransport(self.config, client=http_client)
        resources: DefaultResources = build_default_resources(self.transport)
        self.clock = resources["clock"]
        self.customers = resources["customers"]
        self.entries = resources["entries"]
        self.entry_texts = resources["entry_texts"]
        self.entry_groups = resources["entry_groups"]
        self.lump_sum_services = resources["lump_sum_services"]
        self.projects = resources["projects"]
        self.services = resources["services"]
        self.surcharges = resources["surcharges"]
        self.teams = resources["teams"]
        self.users = resources["users"]
        self.users_nonbusiness_groups = resources["users_nonbusiness_groups"]
        self.user_access = resources["user_access"]
        self.aggregates = resources["aggregates"]
        self.work_times = resources["work_times"]

    @classmethod
    def from_config(
        cls,
        config: ClockodoClientConfig,
        *,
        http_client: httpx.Client | None = None,
    ) -> "ClockodoClient":
        return cls(
            api_user=config.auth.api_user,
            api_key=config.auth.api_key,
            application_name=config.auth.application_name,
            application_contact=config.auth.application_contact,
            base_url=config.base_url,
            timeout=config.timeout,
            language=config.language,
            http_client=http_client,
        )

    @staticmethod
    def endpoint_inventory() -> tuple[Any, ...]:
        return ENDPOINT_INVENTORY

    def close(self) -> None:
        self.transport.close()

    def __enter__(self) -> "ClockodoClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
