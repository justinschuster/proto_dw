import logging
from collections.abc import Iterator
from typing import Any, cast

import dlt
from dlt.common.typing import StrAny, TDataItems
from dlt.sources.helpers.requests import client

logger = logging.getLogger(__name__)


@dlt.source
def example_source(base_url: str = dlt.config.value) -> Any:

    def _get_json(path: str) -> StrAny:
        logger.info(f"Fetching Example Source endpoint path={path}")
        response = client.get(f"{base_url}{path}")
        payload = cast("StrAny", response.json())
        logger.info(f"Fetched Example Source endpoint path={path}")
        return payload

    @dlt.resource(
        name="example_resource",
        primary_key="code",
        write_disposition="merge",
    )
    def get_example_resource() -> Iterator[TDataItems]:
        codes = _get_json("references/example/")["example_key"]
        logger.info(f"Fetched {len(codes)} records")
        if not codes:
            msg = "Example endpoint returned no records"
            logger.error(msg)
            raise ValueError(msg)

        yield from codes

    return get_example_resource()
