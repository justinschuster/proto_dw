import logging
from typing import Any

import pytest
from dlt.extract.exceptions import ResourceExtractionError

from extract.usaspending import extract_usaspending


class FakeResponse:
    def json(self) -> dict[str, list[dict[str, Any]]]:
        return {"codes": [{"code": "L", "title": "CARES Act"}]}


class EmptyResponse:
    def json(self) -> dict[str, list[dict[str, Any]]]:
        return {"codes": []}


def test_usaspending_def_codes_requests_expected_endpoint(
    caplog: Any,
    monkeypatch: Any,
) -> None:
    calls: list[str] = []

    def fake_get(url: str) -> FakeResponse:
        calls.append(url)
        return FakeResponse()

    monkeypatch.setattr(extract_usaspending.client, "get", fake_get)
    caplog.set_level(logging.INFO, logger=extract_usaspending.__name__)

    source = extract_usaspending.usaspending(base_url="https://example.test/api/v2/")

    assert list(source.resources["def_codes"]) == [{"code": "L", "title": "CARES Act"}]
    assert calls == ["https://example.test/api/v2/references/def_codes/"]
    assert "Fetching USAspending endpoint path=references/def_codes/" in caplog.text
    assert "Fetched 1 DEFC records" in caplog.text


def test_usaspending_def_codes_fails_on_empty_response(monkeypatch: Any) -> None:
    def fake_get(url: str) -> EmptyResponse:
        return EmptyResponse()

    monkeypatch.setattr(extract_usaspending.client, "get", fake_get)

    source = extract_usaspending.usaspending(base_url="https://example.test/api/v2/")

    with pytest.raises(
        ResourceExtractionError, match="DEFC endpoint returned no records"
    ):
        list(source.resources["def_codes"])


def test_def_codes_resource_is_idempotent_reference_config() -> None:
    source = extract_usaspending.usaspending()
    resource = source.resources["def_codes"]
    schema = resource.compute_table_schema()

    assert resource.name == "def_codes"
    assert resource.write_disposition == "merge"
    columns = schema.get("columns")
    assert columns is not None
    assert columns["code"]["primary_key"] is True
    assert columns["urls"]["data_type"] == "json"
