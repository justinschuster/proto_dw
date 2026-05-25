import logging
from typing import Any

import pytest
from dlt.extract.exceptions import ResourceExtractionError

from extract.usaspending import extract_usaspending


class FakeResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    def json(self) -> dict[str, Any]:
        return self.payload


DEF_CODES_PAYLOAD: dict[str, list[dict[str, Any]]] = {
    "codes": [{"code": "L", "title": "CARES Act"}]
}
EMPTY_DEF_CODES_PAYLOAD: dict[str, list[dict[str, Any]]] = {"codes": []}


def test_usaspending_def_codes_requests_expected_endpoint(
    caplog: Any,
    monkeypatch: Any,
) -> None:
    calls: list[str] = []

    def fake_get(url: str, params: dict[str, Any] | None = None) -> FakeResponse:
        assert params is None
        calls.append(url)
        return FakeResponse(DEF_CODES_PAYLOAD)

    monkeypatch.setattr(extract_usaspending.client, "get", fake_get)  # type: ignore[attr-defined]
    caplog.set_level(logging.INFO, logger=extract_usaspending.__name__)

    source = extract_usaspending.usaspending(base_url="https://example.test/api/v2/")

    assert list(source.resources["def_codes"]) == [{"code": "L", "title": "CARES Act"}]
    assert calls == ["https://example.test/api/v2/references/def_codes/"]
    assert "Fetching USAspending endpoint path=references/def_codes/" in caplog.text
    assert "Fetched 1 DEFC records" in caplog.text


def test_usaspending_def_codes_fails_on_empty_response(monkeypatch: Any) -> None:
    def fake_get(url: str, params: dict[str, Any] | None = None) -> FakeResponse:
        assert params is None
        return FakeResponse(EMPTY_DEF_CODES_PAYLOAD)

    monkeypatch.setattr(extract_usaspending.client, "get", fake_get)  # type: ignore[attr-defined]

    source = extract_usaspending.usaspending(base_url="https://example.test/api/v2/")

    with pytest.raises(ResourceExtractionError, match="DEFC endpoint returned no records"):
        list(source.resources["def_codes"])


def test_def_codes_resource_is_idempotent_reference_config() -> None:
    source = extract_usaspending.usaspending()
    resource = source.resources["def_codes"]
    schema = resource.compute_table_schema()

    assert resource.name == "def_codes"
    assert resource.write_disposition == "append"
    columns = schema.get("columns")
    assert columns is not None
    assert columns["code"]["primary_key"] is True
    assert columns["urls"]["data_type"] == "json"


def test_usaspending_agency_awards_count_paginates_and_yields_raw_pages(
    caplog: Any,
    monkeypatch: Any,
) -> None:
    calls: list[tuple[str, dict[str, Any] | None]] = []
    page_1 = {
        "results": [[{"awarding_toptier_agency_code": "097", "contracts": 1}]],
        "page_metadata": {
            "page": 1,
            "total": 2,
            "limit": 1,
            "next": 2,
            "previous": None,
            "hasNext": True,
            "hasPrevious": False,
        },
        "messages": [],
    }
    page_2 = {
        "results": [[{"awarding_toptier_agency_code": "012", "contracts": 2}]],
        "page_metadata": {
            "page": 2,
            "total": 2,
            "limit": 1,
            "next": None,
            "previous": 1,
            "hasNext": False,
            "hasPrevious": True,
        },
        "messages": [],
    }

    def fake_get(url: str, params: dict[str, Any] | None = None) -> FakeResponse:
        calls.append((url, params))
        if params == {"page": 1}:
            return FakeResponse(page_1)
        if params == {"page": 2}:
            return FakeResponse(page_2)
        raise AssertionError(f"Unexpected request params: {params}")

    monkeypatch.setattr(extract_usaspending.client, "get", fake_get)  # type: ignore[attr-defined]
    caplog.set_level(logging.INFO, logger=extract_usaspending.__name__)

    source = extract_usaspending.usaspending(base_url="https://example.test/api/v2/")

    assert list(source.resources["agency_awards_count"]) == [page_1, page_2]
    assert calls == [
        ("https://example.test/api/v2/agency/awards/count/", {"page": 1}),
        ("https://example.test/api/v2/agency/awards/count/", {"page": 2}),
    ]
    assert "Fetched agency awards count page=1" in caplog.text
    assert "Fetched agency awards count page=2" in caplog.text


def test_usaspending_agency_awards_count_fails_on_missing_page_metadata(
    monkeypatch: Any,
) -> None:
    def fake_get(url: str, params: dict[str, Any] | None = None) -> FakeResponse:
        return FakeResponse({"results": [], "messages": []})

    monkeypatch.setattr(extract_usaspending.client, "get", fake_get)  # type: ignore[attr-defined]

    source = extract_usaspending.usaspending(base_url="https://example.test/api/v2/")

    with pytest.raises(
        ResourceExtractionError,
        match="Agency awards count endpoint returned invalid page metadata",
    ):
        list(source.resources["agency_awards_count"])


def test_agency_awards_count_resource_is_raw_append_config() -> None:
    source = extract_usaspending.usaspending()
    resource = source.resources["agency_awards_count"]
    schema = resource.compute_table_schema()

    assert resource.name == "agency_awards_count"
    assert resource.write_disposition == "append"
    assert schema.get("columns") == {}
