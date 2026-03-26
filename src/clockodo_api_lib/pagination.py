from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class Paging(BaseModel):
    model_config = ConfigDict(extra="allow")

    items_per_page: int
    current_page: int
    count_pages: int
    count_items: int


class CollectionResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(extra="allow")

    items: list[T]
    paging: Paging | None = None
