from __future__ import annotations

from typing import Any, Iterable, Sequence

from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import InstrumentedAttribute, Query


def apply_text_search(
    query: Query,
    columns: Sequence[InstrumentedAttribute[Any]],
    term: str | None,
) -> Query:
    if term:
        pattern = f"%{term.strip()}%"
        conditions = [column.ilike(pattern) for column in columns]
        if conditions:
            query = query.filter(or_(*conditions))
    return query


def resolve_sort(
    sort: str | None,
    allowed: dict[str, InstrumentedAttribute[Any]],
    default: str,
) -> list[Any]:
    tokens = [token.strip() for token in (sort or default).split(",") if token.strip()]
    order_by_clauses: list[Any] = []
    for token in tokens:
        direction = desc if token.startswith("-") else asc
        field_name = token[1:] if token[0] in "-+" else token
        column = allowed.get(field_name)
        if column is None:
            continue
        order_by_clauses.append(direction(column))
    if not order_by_clauses and default:
        field_name = default[1:] if default.startswith(("-", "+")) else default
        column = allowed.get(field_name)
        if column is not None:
            direction = desc if default.startswith("-") else asc
            order_by_clauses.append(direction(column))
    return order_by_clauses


def paginate(query: Query, page: int, page_size: int) -> tuple[list[Any], int]:
    total = query.order_by(None).count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return items, total
