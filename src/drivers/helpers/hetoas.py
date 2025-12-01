from typing import Any, Dict, List

from fastapi import Request
from pydantic import BaseModel, PositiveInt

from domain.value_objects.ordering import Ordering


class ListingParams(BaseModel):
    page: PositiveInt = 1
    limit: PositiveInt = 10
    order_by: str = "created_at"
    ordering: Ordering = Ordering.ASC


def create_hateoas_response(
    request: Request,
    listing_params: ListingParams,
    items: List[Dict[str, Any]],
    total_count: int,
) -> Dict[str, Any]:
    links = build_pagination_links(
        request, listing_params.page, listing_params.limit, total_count
    )

    return {
        "items": items,
        "total_count": total_count,
        "page": listing_params.page,
        "limit": listing_params.limit,
        "links": links,
    }


def build_pagination_links(
    request: Request,
    page: int,
    limit: int,
    total_count: int,
) -> dict:
    # Get base URL and path
    base_url = str(request.url.remove_query_params(["page", "limit"]))

    # Get existing query parameters (excluding page and limit)
    query_params = dict(request.query_params)
    query_params.pop("page", None)
    query_params.pop("limit", None)

    # Build query string from remaining params
    extra_params = "&".join(f"{k}={v}" for k, v in query_params.items())
    separator = "&" if extra_params else ""

    # Calculate total pages
    total_pages = (total_count + limit - 1) // limit if total_count > 0 else 1

    # Build links
    links = {
        "first": f"{base_url}?page=1&limit={limit}{separator}{extra_params}",
        "last": f"{base_url}?page={total_pages}&limit={limit}{separator}{extra_params}",
    }

    # Add next link if not on last page
    if page < total_pages:
        links["next"] = (
            f"{base_url}?page={page + 1}&limit={limit}{separator}{extra_params}"
        )

    # Add previous link if not on first page
    if page > 1:
        links["previous"] = (
            f"{base_url}?page={page - 1}&limit={limit}{separator}{extra_params}"
        )

    return links
