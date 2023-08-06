from typing import Optional, Any, Type, Callable, TYPE_CHECKING

from fastapi import Depends, Query, Request
from pydantic import NonNegativeInt

from fastapi_all_out.pydantic import CommaSeparatedOf, snake_case

if TYPE_CHECKING:
    from fastapi_all_out.routers.filters import BaseFilter


ROUTE = bool | dict[str, Any]
PAGINATION = tuple[Optional[int], Optional[int]]
FILTERS = list["BaseFilter"]
SORT = list[str]


def pagination_factory(max_limit: Optional[int], default_limit: Optional[int] = 50) -> Any:
    """
    Created the pagination dependency to be used in the CRUDRouter
    """

    if max_limit and default_limit > max_limit:
        default_limit = max_limit

    def pagination(
            skip: Optional[NonNegativeInt] = Query(None),
            limit: Optional[int] = Query(default_limit, ge=1, le=max_limit)
    ) -> PAGINATION:
        return skip, limit

    return Depends(pagination)


def filters_factory(available_filters: list[Type["BaseFilter"]]):
    def filters(request: Request) -> FILTERS:
        qp = request.query_params
        return [final_f for f in available_filters if (final_f := f.from_qs(qp))]
    return filters


def sort_factory(available: set[str]) -> Callable[[...], list[str]]:
    available_bidirectional: set[str] = set()
    for x in available:
        available_bidirectional.add(x)
        available_bidirectional.add('-' + x)

    def sort(fields: CommaSeparatedOf(str, wrapper=snake_case, in_query=True) = Query(
        None,
        alias='sort',
        description=f'Write,fields,separated,by,commas. Available (also with "-" if descendant): {", ".join(available)}'
    )) -> SORT:
        result: list[str] = []
        if fields:
            for field in fields:
                if field in available_bidirectional:
                    result.append(field)
        return result

    return sort
