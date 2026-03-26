# clockodo-api-lib

Typed Python client for the Clockodo API v2.

The package is managed with `uv`, uses `httpx` for outbound API calls, and uses `pydantic` models for request and response validation.

## API Coverage

The client currently exposes the Clockodo API v2 resource groups captured in [`inventory.py`](./src/clockodo_api_lib/inventory.py):

- `clock`
- `customers`
- `entries`
- `entriesTexts`
- `entrygroups`
- `lumpsumservices`
- `projects`
- `services`
- `surcharges`
- `teams`
- `users`
- `usersNonbusinessGroups`
- `users/access/customers-projects`
- `users/access/services`
- `aggregates/users/me`
- `workTimes`
- `workTimes/changeRequests`

## Install In Another Project

The package name is `clockodo-api-lib`. The Python import path is `clockodo_api_lib`.

### Local path dependency

```bash
cd /path/to/other-project
uv add /home/fabian/documents/_repos/clockodo-api-lib
```

### Editable local dependency

Use this when you want changes in this repository to be reflected immediately in the consuming project.

```bash
cd /path/to/other-project
uv add --editable /home/fabian/documents/_repos/clockodo-api-lib
```

### Built wheel

```bash
cd /home/fabian/documents/_repos/clockodo-api-lib
uv build

cd /path/to/other-project
uv add /home/fabian/documents/_repos/clockodo-api-lib/dist/clockodo_api_lib-*.whl
```

## Use The Library

### Create a client

Import `ClockodoClient` from `clockodo_api_lib`:

```python
from clockodo_api_lib import ClockodoClient
```

The constructor accepts these required authentication values:

- `api_user`: the Clockodo user email used for API authentication
- `api_key`: the Clockodo API key
- `application_name`: the integration name Clockodo should see in request headers
- `application_contact`: a technical contact email for the integration

Optional settings:

- `base_url`: defaults to `https://my.clockodo.com/api/v2`
- `timeout`: defaults to `30.0` seconds
- `language`: defaults to `"en"` and is sent as `Accept-Language`

```python
from clockodo_api_lib import ClockodoClient

with ClockodoClient(
    api_user="api-user@example.com",
    api_key="your-api-key",
    application_name="my-integration",
    application_contact="dev@example.com",
    timeout=15.0,
    language="en",
) as client:
    ...
```

### Find the right resource group

The public API is grouped by resource area on the client instance. Common top-level resources include:

- `client.clock`
- `client.customers`
- `client.entries`
- `client.entry_texts`
- `client.entry_groups`
- `client.projects`
- `client.services`
- `client.teams`
- `client.users`
- `client.work_times`

Nested groups are available as nested attributes:

- `client.user_access.customer_projects`
- `client.user_access.services`
- `client.aggregates.users_me`
- `client.work_times.change_requests`

Each resource exposes methods that match the underlying Clockodo endpoint group, such as `list`, `get`, `create`, `update`, `delete`, or resource-specific methods like `approve`.

### Use typed request and response models

Request bodies and list/query parameter objects live in `clockodo_api_lib.models`. Import the model that matches the endpoint you want to call and pass it directly into the client method.

```python
from clockodo_api_lib.models import CustomerCreateRequest, CustomerFilter, CustomerListParams
```

List endpoints return typed `CollectionResponse[...]` objects with:

- `items`: the parsed result models
- `paging`: pagination metadata when Clockodo returns it

Single-resource endpoints return typed response models such as `Customer`, `Project`, or `UserAggregateResponse`.

### Example: list customers with typed params

```python
from clockodo_api_lib import ClockodoClient
from clockodo_api_lib.models import CustomerFilter, CustomerListParams

with ClockodoClient(
    api_user="api-user@example.com",
    api_key="your-api-key",
    application_name="my-integration",
    application_contact="dev@example.com",
) as client:
    customers = client.customers.list(
        CustomerListParams(page=1, filter=CustomerFilter(active=True))
    )

    for customer in customers.items:
        print(customer.id, customer.name)

    if customers.paging is not None:
        print(
            customers.paging.current_page,
            customers.paging.count_pages,
            customers.paging.count_items,
        )
```

### Example: create a customer

```python
from clockodo_api_lib import ClockodoClient
from clockodo_api_lib.models import CustomerCreateRequest

with ClockodoClient(
    api_user="api-user@example.com",
    api_key="your-api-key",
    application_name="my-integration",
    application_contact="dev@example.com",
) as client:
    customer = client.customers.create(
        CustomerCreateRequest(name="Acme GmbH", number="C-100")
    )

    print(customer.id, customer.name)
```

### Example: call nested resource groups

```python
from clockodo_api_lib import ClockodoClient

with ClockodoClient(
    api_user="api-user@example.com",
    api_key="your-api-key",
    application_name="my-integration",
    application_contact="dev@example.com",
) as client:
    aggregate = client.aggregates.users_me.get()
    rights = client.user_access.services.get(user_id=123)

    print(aggregate.user.name)
    print(rights.add)
```

## Development

Contributor setup is separate from consumer usage.

### Install development dependencies

```bash
uv sync --group dev
```

### Run tests

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest
```

### Validate downstream `uv` installation flows

```bash
UV_CACHE_DIR=/tmp/uv-cache ./scripts/validate_uv_package_consumption.sh
```
