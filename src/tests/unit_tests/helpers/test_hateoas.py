import pytest
from unittest.mock import Mock
from httpx import QueryParams

from drivers.helpers.hetoas import ListingParams, create_hateoas_response


@pytest.fixture
def mock_request():
    def _create_request(url: str, query_params: dict = None):
        request = Mock()
        request.url = Mock()
        request.url.__str__ = Mock(return_value=url)
        request.url.remove_query_params = Mock(return_value=Mock(__str__=Mock(return_value=url.split("?")[0])))
        request.query_params = QueryParams(query_params or {})
        return request
    return _create_request


@pytest.fixture
def sample_items():
    return [
        {"id": "1", "title": "Task 1"},
        {"id": "2", "title": "Task 2"},
    ]


@pytest.mark.asyncio
async def test_create_hateoas_response_first_page_with_next(mock_request, sample_items):
    request = mock_request("http://test/api/v1/tasks", {"page": "1", "limit": "2"})
    listing_params = ListingParams(page=1, limit=2)
    total_count = 10

    result = create_hateoas_response(request, listing_params, sample_items, total_count)

    assert result["items"] == sample_items
    assert result["total_count"] == 10
    assert result["page"] == 1
    assert result["limit"] == 2
    assert "first" in result["links"]
    assert "last" in result["links"]
    assert "next" in result["links"]
    assert "previous" not in result["links"]


@pytest.mark.asyncio
async def test_create_hateoas_response_middle_page_with_next_and_previous(mock_request, sample_items):
    request = mock_request("http://test/api/v1/tasks", {"page": "2", "limit": "2"})
    listing_params = ListingParams(page=2, limit=2)
    total_count = 10

    result = create_hateoas_response(request, listing_params, sample_items, total_count)

    assert result["items"] == sample_items
    assert result["total_count"] == 10
    assert result["page"] == 2
    assert result["limit"] == 2
    assert "first" in result["links"]
    assert "last" in result["links"]
    assert "next" in result["links"]
    assert "previous" in result["links"]


@pytest.mark.asyncio
async def test_create_hateoas_response_last_page_with_previous(mock_request, sample_items):
    request = mock_request("http://test/api/v1/tasks", {"page": "5", "limit": "2"})
    listing_params = ListingParams(page=5, limit=2)
    total_count = 10

    result = create_hateoas_response(request, listing_params, sample_items, total_count)

    assert result["items"] == sample_items
    assert result["total_count"] == 10
    assert result["page"] == 5
    assert result["limit"] == 2
    assert "first" in result["links"]
    assert "last" in result["links"]
    assert "previous" in result["links"]
    assert "next" not in result["links"]


@pytest.mark.asyncio
async def test_create_hateoas_response_single_page_no_next_or_previous(mock_request, sample_items):
    request = mock_request("http://test/api/v1/tasks", {"page": "1", "limit": "10"})
    listing_params = ListingParams(page=1, limit=10)
    total_count = 2

    result = create_hateoas_response(request, listing_params, sample_items, total_count)

    assert result["items"] == sample_items
    assert result["total_count"] == 2
    assert result["page"] == 1
    assert result["limit"] == 10
    assert "first" in result["links"]
    assert "last" in result["links"]
    assert "next" not in result["links"]
    assert "previous" not in result["links"]


@pytest.mark.asyncio
async def test_create_hateoas_response_with_filters(mock_request, sample_items):
    request = mock_request(
        "http://test/api/v1/tasks",
        {"page": "1", "limit": "2", "status_filter": "pending", "priority_filter": "high"}
    )
    listing_params = ListingParams(page=1, limit=2)
    total_count = 6

    result = create_hateoas_response(request, listing_params, sample_items, total_count)

    assert result["items"] == sample_items
    assert result["total_count"] == 6
    assert result["page"] == 1
    assert result["limit"] == 2

    assert "first" in result["links"]
    assert "page=1" in result["links"]["first"]
    assert "limit=2" in result["links"]["first"]
    assert "status_filter=pending" in result["links"]["first"]
    assert "priority_filter=high" in result["links"]["first"]

    assert "next" in result["links"]
    assert "page=2" in result["links"]["next"]
    assert "status_filter=pending" in result["links"]["next"]
    assert "priority_filter=high" in result["links"]["next"]


@pytest.mark.asyncio
async def test_create_hateoas_response_empty_list(mock_request):
    request = mock_request("http://test/api/v1/tasks", {"page": "1", "limit": "10"})
    listing_params = ListingParams(page=1, limit=10)
    total_count = 0

    result = create_hateoas_response(request, listing_params, [], total_count)

    assert result["items"] == []
    assert result["total_count"] == 0
    assert result["page"] == 1
    assert result["limit"] == 10
    assert "first" in result["links"]
    assert "last" in result["links"]
    assert "next" not in result["links"]
    assert "previous" not in result["links"]
