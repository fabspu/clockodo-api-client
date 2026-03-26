from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EndpointOperation:
    public_path: tuple[str, ...]
    method_name: str
    http_method: str
    path_template: str


ENDPOINT_INVENTORY: tuple[EndpointOperation, ...] = (
    EndpointOperation(("clock",), "get_running", "GET", "/clock"),
    EndpointOperation(("clock",), "start", "POST", "/clock"),
    EndpointOperation(("clock",), "stop", "DELETE", "/clock/{entry_id}"),
    EndpointOperation(("clock",), "change_duration", "PUT", "/clock/{entry_id}"),
    EndpointOperation(("customers",), "list", "GET", "/customers"),
    EndpointOperation(("customers",), "get", "GET", "/customers/{resource_id}"),
    EndpointOperation(("customers",), "create", "POST", "/customers"),
    EndpointOperation(("customers",), "update", "PUT", "/customers/{resource_id}"),
    EndpointOperation(("customers",), "delete", "DELETE", "/customers/{resource_id}"),
    EndpointOperation(("entries",), "list", "GET", "/entries"),
    EndpointOperation(("entries",), "get", "GET", "/entries/{resource_id}"),
    EndpointOperation(("entries",), "create", "POST", "/entries"),
    EndpointOperation(("entries",), "update", "PUT", "/entries/{resource_id}"),
    EndpointOperation(("entries",), "delete", "DELETE", "/entries/{resource_id}"),
    EndpointOperation(("entry_texts",), "list", "GET", "/entriesTexts"),
    EndpointOperation(("entry_groups",), "list", "GET", "/entrygroups"),
    EndpointOperation(("entry_groups",), "update", "PUT", "/entrygroups"),
    EndpointOperation(("entry_groups",), "delete", "DELETE", "/entrygroups"),
    EndpointOperation(("lump_sum_services",), "list", "GET", "/lumpsumservices"),
    EndpointOperation(("lump_sum_services",), "get", "GET", "/lumpsumservices/{resource_id}"),
    EndpointOperation(("lump_sum_services",), "create", "POST", "/lumpsumservices"),
    EndpointOperation(("lump_sum_services",), "update", "PUT", "/lumpsumservices/{resource_id}"),
    EndpointOperation(("lump_sum_services",), "delete", "DELETE", "/lumpsumservices/{resource_id}"),
    EndpointOperation(("projects",), "list", "GET", "/projects"),
    EndpointOperation(("projects",), "get", "GET", "/projects/{resource_id}"),
    EndpointOperation(("projects",), "create", "POST", "/projects"),
    EndpointOperation(("projects",), "update", "PUT", "/projects/{resource_id}"),
    EndpointOperation(("projects",), "delete", "DELETE", "/projects/{resource_id}"),
    EndpointOperation(("services",), "list", "GET", "/services"),
    EndpointOperation(("services",), "get", "GET", "/services/{resource_id}"),
    EndpointOperation(("services",), "create", "POST", "/services"),
    EndpointOperation(("services",), "update", "PUT", "/services/{resource_id}"),
    EndpointOperation(("services",), "delete", "DELETE", "/services/{resource_id}"),
    EndpointOperation(("surcharges",), "list", "GET", "/surcharges"),
    EndpointOperation(("surcharges",), "get", "GET", "/surcharges/{resource_id}"),
    EndpointOperation(("surcharges",), "create", "POST", "/surcharges"),
    EndpointOperation(("surcharges",), "update", "PUT", "/surcharges/{resource_id}"),
    EndpointOperation(("surcharges",), "delete", "DELETE", "/surcharges/{resource_id}"),
    EndpointOperation(("teams",), "list", "GET", "/teams"),
    EndpointOperation(("teams",), "get", "GET", "/teams/{resource_id}"),
    EndpointOperation(("teams",), "create", "POST", "/teams"),
    EndpointOperation(("teams",), "update", "PUT", "/teams/{resource_id}"),
    EndpointOperation(("teams",), "delete", "DELETE", "/teams/{resource_id}"),
    EndpointOperation(("users",), "list", "GET", "/users"),
    EndpointOperation(("users",), "get", "GET", "/users/{resource_id}"),
    EndpointOperation(("users",), "create", "POST", "/users"),
    EndpointOperation(("users",), "update", "PUT", "/users/{resource_id}"),
    EndpointOperation(("users",), "delete", "DELETE", "/users/{resource_id}"),
    EndpointOperation(("users_nonbusiness_groups",), "list", "GET", "/usersNonbusinessGroups"),
    EndpointOperation(("users_nonbusiness_groups",), "get", "GET", "/usersNonbusinessGroups/{resource_id}"),
    EndpointOperation(("users_nonbusiness_groups",), "create", "POST", "/usersNonbusinessGroups"),
    EndpointOperation(("users_nonbusiness_groups",), "update", "PUT", "/usersNonbusinessGroups/{resource_id}"),
    EndpointOperation(("users_nonbusiness_groups",), "delete", "DELETE", "/usersNonbusinessGroups/{resource_id}"),
    EndpointOperation(("user_access", "customer_projects"), "get", "GET", "/users/{user_id}/access/customers-projects"),
    EndpointOperation(("user_access", "services"), "get", "GET", "/users/{user_id}/access/services"),
    EndpointOperation(("aggregates", "users_me"), "get", "GET", "/aggregates/users/me"),
    EndpointOperation(("work_times",), "list", "GET", "/workTimes"),
    EndpointOperation(("work_times", "change_requests"), "list", "GET", "/workTimes/changeRequests"),
    EndpointOperation(("work_times", "change_requests"), "create", "POST", "/workTimes/changeRequests"),
    EndpointOperation(("work_times", "change_requests"), "approve", "POST", "/workTimes/changeRequests/{resource_id}/approve"),
    EndpointOperation(("work_times", "change_requests"), "decline", "POST", "/workTimes/changeRequests/{resource_id}/decline"),
    EndpointOperation(("work_times", "change_requests"), "delete", "DELETE", "/workTimes/changeRequests/{resource_id}"),
)
