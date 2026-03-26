from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ClockodoModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class SuccessResponse(ClockodoModel):
    success: bool


class Customer(ClockodoModel):
    id: int
    name: str
    number: str | None = None
    active: bool | None = None
    billable_default: bool | None = None
    note: str | None = None
    color: int | None = None


class Project(ClockodoModel):
    id: int
    customers_id: int
    name: str
    number: str | None = None
    active: bool | None = None
    billable_default: bool | None = None
    note: str | None = None
    budget_money: float | None = None
    budget_is_hours: bool | None = None
    budget_is_not_strict: bool | None = None
    completed: bool | None = None
    billed_money: float | None = None
    billed_completely: bool | None = None
    revenue_factor: float | None = None
    deadline: str | None = None


class Service(ClockodoModel):
    id: int
    name: str
    number: str | None = None
    active: bool | None = None
    note: str | None = None


class LumpSumService(ClockodoModel):
    id: int
    name: str
    price: float
    unit: str | None = None
    number: str | None = None
    active: bool | None = None
    note: str | None = None


class Team(ClockodoModel):
    id: int
    name: str
    leader: int | None = None


class User(ClockodoModel):
    id: int
    name: str
    email: str | None = None
    role: str | None = None
    active: bool | None = None
    number: str | None = None
    language: str | None = None
    timezone: str | None = None
    teams_id: int | None = None
    boss: int | None = None


class Entry(ClockodoModel):
    id: int
    customers_id: int | None = None
    projects_id: int | None = None
    services_id: int | None = None
    lumpsum_services_id: int | None = None
    users_id: int | None = None
    billable: int | None = None
    text: str | None = None
    time_since: str | None = None
    time_until: str | None = None
    duration: int | None = None
    hourly_rate: float | None = None
    lumpsum: float | None = None
    lumpsum_services_amount: float | None = None


class EntryGroup(ClockodoModel):
    grouped_by: str | None = None
    group: str | None = None
    name: str | None = None
    number: str | None = None
    note: str | None = None
    subgroups: list["EntryGroup"] = Field(default_factory=list)


class Surcharge(ClockodoModel):
    percent: int
    time_since: str
    time_until: str
    time_since_is_previous_day: bool | None = None
    time_until_is_next_day: bool | None = None


class SurchargeModel(ClockodoModel):
    id: int
    name: str
    accumulation: bool
    night: Surcharge | None = None
    night_increased: Surcharge | None = None
    nonbusiness: Surcharge | None = None
    nonbusiness_special: Surcharge | None = None
    sunday: Surcharge | None = None
    saturday: Surcharge | None = None


class UserNonbusinessGroup(ClockodoModel):
    id: int
    users_id: int
    nonbusiness_groups_id: int
    date_since: str
    date_until: str | None = None


class WorkTimeInterval(ClockodoModel):
    time_since: str
    time_until: str


class WorkTimeDay(ClockodoModel):
    date: str
    users_id: int
    offset: int | None = None
    intervals: list[WorkTimeInterval] = Field(default_factory=list)


class ChangeRequestInterval(ClockodoModel):
    type: Literal[1, 2]
    time_since: str
    time_until: str


class ChangeRequest(ClockodoModel):
    id: int
    date: str
    users_id: int
    status: int
    declined_at: str | None = None
    declined_by: int | None = None
    changes: list[ChangeRequestInterval] = Field(default_factory=list)


class Company(ClockodoModel):
    id: int
    name: str
    timezone_default: str | None = None
    currency: str | None = None
    allow_entries_multiline: bool | None = None
    allow_entries_for_customers: bool | None = None
    force_linked_entry_times: bool | None = None
    default_customers_id: int | None = None
    default_services_id: int | None = None
    module_absence: bool | None = None
    module_work_time: bool | None = None
    nonbusiness_group_default: int | None = None
    worktime_regulation_default: int | None = None


class BreakRule(ClockodoModel):
    worktime: float
    break_sum: int
    splitting: dict[str, int] | None = None


class WorktimeRegulation(ClockodoModel):
    id: int
    add_to_worktime: bool | None = None
    weekly_max: float | None = None
    daily_max: float | None = None
    interval_max: float | None = None
    rules: list[BreakRule] = Field(default_factory=list)


class UserAggregateResponse(ClockodoModel):
    user: User
    company: Company
    worktime_regulation: WorktimeRegulation | None = None


class CustomerProjectAccessResponse(ClockodoModel):
    add: bool | dict[str, Any]
    report: bool | dict[str, Any]
    edit: bool | dict[str, Any]


class ServiceAccessResponse(ClockodoModel):
    add: bool | dict[str, bool]


class EntryTextSearchResponse(ClockodoModel):
    paging: Any | None = None
    filter: dict[str, Any] | None = None
    mode: str | None = None
    sort: str | None = None
    texts: dict[str, str] = Field(default_factory=dict)


class EntryGroupMutationPreview(ClockodoModel):
    confirm_key: str
    affected_entries: int


class EntryGroupMutationResult(ClockodoModel):
    success: bool
    edited_entries: int | None = None
    deleted_entries: int | None = None


class ClockRunningResponse(ClockodoModel):
    running: Entry | None = None


class ClockStopResponse(ClockodoModel):
    stopped: Entry | None = None
    running: Entry | None = None


class ClockDurationResponse(ClockodoModel):
    updated: Entry | None = None
    running: Entry | None = None


class ChangeRequestCreateResponse(ClockodoModel):
    change_request: ChangeRequest | None = None
    replaced_change_request: ChangeRequest | None = None
    approved_immediately: bool | None = None


class CustomerFilter(ClockodoModel):
    active: bool | None = None


class CustomerListParams(ClockodoModel):
    page: int | None = None
    filter: CustomerFilter | None = None


class CustomerCreateRequest(ClockodoModel):
    name: str
    number: str | None = None
    active: bool | None = None
    billable_default: bool | None = None
    note: str | None = None


class CustomerUpdateRequest(ClockodoModel):
    name: str | None = None
    number: str | None = None
    active: bool | None = None
    billable_default: bool | None = None
    note: str | None = None


class ProjectFilter(ClockodoModel):
    customers_id: int | None = None
    active: bool | None = None


class ProjectListParams(ClockodoModel):
    page: int | None = None
    filter: ProjectFilter | None = None


class ProjectCreateRequest(ClockodoModel):
    name: str
    customers_id: int
    number: str | None = None
    active: bool | None = None
    billable_default: bool | None = None
    budget_money: float | None = None
    budget_is_hours: bool | None = None
    budget_is_not_strict: bool | None = None
    note: str | None = None
    deadline: str | None = None


class ProjectUpdateRequest(ClockodoModel):
    name: str | None = None
    customers_id: int | None = None
    number: str | None = None
    active: bool | None = None
    billable_default: bool | None = None
    budget_money: float | None = None
    budget_is_hours: bool | None = None
    budget_ist_not_strict: bool | None = None
    note: str | None = None
    completed: bool | None = None
    billed_money: float | None = None
    billed_completely: bool | None = None
    deadline: str | None = None


class ServiceCreateRequest(ClockodoModel):
    name: str
    number: str | None = None
    active: bool | None = None
    note: str | None = None


class ServiceUpdateRequest(ServiceCreateRequest):
    name: str | None = None


class LumpSumServiceCreateRequest(ClockodoModel):
    name: str
    price: float
    unit: str | None = None
    number: str | None = None
    active: bool | None = None
    note: str | None = None


class LumpSumServiceUpdateRequest(LumpSumServiceCreateRequest):
    name: str | None = None
    price: float | None = None


class TeamCreateRequest(ClockodoModel):
    name: str
    leader: int | None = None


class TeamUpdateRequest(ClockodoModel):
    name: str | None = None
    leader: int | None = None


class UserCreateRequest(ClockodoModel):
    name: str
    email: str
    role: str
    mail_to_user: bool | None = None
    number: str | None = None
    timeformat_12h: bool | None = None
    weekstart_monday: bool | None = None
    weekend_friday: bool | None = None
    language: str | None = None
    timezone: str | None = None
    wage_type: int | None = None
    can_generally_see_absences: bool | None = None
    can_generally_manage_absences: bool | None = None
    can_add_customers: bool | None = None
    edit_lock_sync: bool | None = None
    teams_id: int | None = None
    nonbusinessgroups_id: int | None = None
    worktime_regulation_id: int | None = None
    boss: int | None = None


class UserUpdateRequest(ClockodoModel):
    name: str | None = None
    number: str | None = None
    active: bool | None = None
    role: str | None = None
    timeformat_12h: bool | None = None
    weekstart_monday: bool | None = None
    weekend_friday: bool | None = None
    language: str | None = None
    timezone: str | None = None
    wage_type: int | None = None
    can_generally_see_absences: bool | None = None
    can_generally_manage_absences: bool | None = None
    can_add_customers: bool | None = None
    edit_lock: str | None = None
    edit_lock_dyn: int | None = None
    edit_lock_sync: bool | None = None
    teams_id: int | None = None
    nonbusinessgroups_id: int | None = None
    worktime_regulation_id: int | None = None
    boss: int | None = None


class EntryFilter(ClockodoModel):
    users_id: int | list[int] | None = None
    customers_id: int | list[int] | None = None
    projects_id: int | list[int] | None = None
    services_id: int | list[int] | None = None
    lumpsum_services_id: int | list[int] | None = None
    billable: int | None = None
    text: str | None = None
    texts_id: int | None = None
    budget_type: str | None = None


class EntryListParams(ClockodoModel):
    time_since: str
    time_until: str
    page: int | None = None
    filter: EntryFilter | None = None
    calc_also_revenues_for_projects_with_hard_budget: bool | None = None
    enhanced_list: bool | None = None


class EntryCreateRequest(ClockodoModel):
    customers_id: int
    services_id: int | None = None
    lumpsum_services_id: int | None = None
    lumpsum_services_amount: float | None = None
    billable: int
    time_since: str
    time_until: str | None = None
    duration: int | None = None
    hourly_rate: float | None = None
    projects_id: int | None = None
    text: str | None = None
    users_id: int | None = None
    lumpsum: float | None = None


class EntryUpdateRequest(ClockodoModel):
    customers_id: int | None = None
    projects_id: int | None = None
    services_id: int | None = None
    lumpsum_services_id: int | None = None
    users_id: int | None = None
    billable: int | None = None
    text: str | None = None
    duration: int | None = None
    lumpsum: float | None = None
    lumpsum_services_amount: float | None = None
    hourly_rate: float | None = None
    time_since: str | None = None
    time_until: str | None = None


class EntryTextsListParams(ClockodoModel):
    text: str
    mode: str | None = None
    sort: str | None = None
    page: int | None = None
    filter: EntryFilter | None = None


class EntryGroupListRequest(ClockodoModel):
    time_since: str
    time_until: str
    grouping: list[str]
    filter: EntryFilter | None = None
    round_to_minutes: int | None = None
    prepend_customer_to_project_name: bool | None = None
    calc_also_revenues_for_projects_with_hard_budget: bool | None = None


class EntryGroupUpdateRequest(ClockodoModel):
    time_since: str
    time_until: str
    filter: EntryFilter | None = None
    projects_id: int | None = None
    services_id: int | None = None
    lumpsum_services_id: int | None = None
    billable: int | None = None
    text: str | None = None
    hourly_rate: float | None = None
    confirm_key: str | None = None


class EntryGroupDeleteRequest(ClockodoModel):
    time_since: str
    time_until: str
    filter: EntryFilter | None = None
    confirm_key: str | None = None


class ClockStartRequest(ClockodoModel):
    customers_id: int
    services_id: int
    billable: int | None = None
    projects_id: int | None = None
    text: str | None = None
    users_id: int | None = None


class ClockDurationChangeRequest(ClockodoModel):
    duration_before: int
    duration: int


class SurchargeModelCreateRequest(ClockodoModel):
    name: str
    accumulation: bool
    night: Surcharge | None = None
    night_increased: Surcharge | None = None
    nonbusiness: Surcharge | None = None
    nonbusiness_special: Surcharge | None = None
    sunday: Surcharge | None = None
    saturday: Surcharge | None = None


class SurchargeModelUpdateRequest(ClockodoModel):
    name: str | None = None
    accumulation: bool | None = None
    night: Surcharge | None = None
    night_increased: Surcharge | None = None
    nonbusiness: Surcharge | None = None
    nonbusiness_special: Surcharge | None = None
    sunday: Surcharge | None = None
    saturday: Surcharge | None = None


class UserNonbusinessGroupListFilter(ClockodoModel):
    users_id: int | list[int] | None = None
    nonbusiness_groups_id: int | list[int] | None = None


class UserNonbusinessGroupListParams(ClockodoModel):
    filter: UserNonbusinessGroupListFilter | None = None


class UserNonbusinessGroupCreateRequest(ClockodoModel):
    users_id: int
    nonbusiness_groups_id: int
    date_since: str
    date_until: str | None = None


class UserNonbusinessGroupUpdateRequest(ClockodoModel):
    nonbusiness_groups_id: int | None = None
    date_since: str | None = None
    date_until: str | None = None


class WorkTimesListParams(ClockodoModel):
    date_since: str
    date_until: str
    users_id: int
    page: int | None = None


class ChangeRequestListParams(ClockodoModel):
    date_since: str | None = None
    date_until: str | None = None
    users_id: int | None = None
    status: int | None = None
    page: int | None = None


class ChangeRequestCreateRequest(ClockodoModel):
    date: str
    users_id: int
    changes: list[ChangeRequestInterval]


EntryGroup.model_rebuild()
