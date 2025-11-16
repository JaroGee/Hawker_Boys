from __future__ import annotations

from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
    items: Sequence[T]
    total: int
    page: int
    page_size: int
