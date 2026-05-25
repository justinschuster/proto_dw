import logging
from collections.abc import Iterator
from typing import Any, cast

import dlt
from dlt.common.typing import StrAny, TDataItems
from dlt.sources.helpers.requests import client

logger = logging.getLogger(__name__)


@dlt.source
def usaspending(base_url: str = dlt.config.value) -> Any:
    """Create a dlt source for USAspending.gov API reference resources.

    Args:
        base_url: Base URL for the USAspending API. By default, dlt resolves
            this from `.dlt/config.toml` under `[sources.usaspending]`.
            Override this in tests or when targeting an alternate
            USAspending-compatible environment.

    Returns:
        A dlt source containing the `def_codes` resource.
    """

    def _get_json(path: str) -> StrAny:
        """Fetch a USAspending API path as JSON.

        Args:
            path: Endpoint path relative to `base_url`, for example
                `references/def_codes/`.

        Returns:
            Parsed JSON response as a string-keyed dictionary.
        """
        logger.info(f"Fetching USAspending endpoint path={path}")
        response = client.get(f"{base_url}{path}")
        payload = cast("StrAny", response.json())
        logger.info(f"Fetched USAspending endpoint path={path}")
        return payload

    @dlt.resource(
        name="def_codes",
        primary_key="code",
        write_disposition="append",
        columns={"urls": {"data_type": "json"}},
    )
    def get_def_codes() -> Iterator[TDataItems]:
        """Yield DEFC reference records from USAspending.gov.

        Returns:
            An iterator of DEFC records selected from the endpoint's `codes`
            array. dlt loads these records into the `def_codes` table.
        """
        codes = _get_json("references/def_codes/")["codes"]
        logger.info(f"Fetched {len(codes)} DEFC records")
        if not codes:
            msg = "DEFC endpoint returned no records"
            logger.error(msg)
            raise ValueError(msg)

        yield from codes

    return get_def_codes()


def load_data(pipeline: Any, data: Any) -> Any:
    """Run a dlt pipeline and log destination-neutral load metadata.

    Args:
        pipeline: Configured dlt pipeline instance.
        data: dlt source or resource data to load.

    Returns:
        dlt load information from the pipeline run.
    """
    logger.info(
        f"Starting USAspending pipeline name={pipeline.pipeline_name} "
        f"dataset={pipeline.dataset_name}"
    )
    try:
        load_info = pipeline.run(data)
    except Exception:
        logger.exception("USAspending pipeline failed")
        raise

    logger.info("Completed USAspending pipeline")
    logger.info(str(load_info))

    logger.info(f"Pipeline was started: {load_info.started_at}")
    normalize_info = pipeline.last_trace.last_normalize_info
    logger.info(f"Normalize row counts: {normalize_info.row_counts}")

    for package in load_info.load_packages:
        if package.schema_update:
            logger.info(f"Schema updated tables: {list(package.schema_update)}")

    return load_info


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="usaspending",
        destination="filesystem",
        dataset_name="usaspending",
    )
    load_data(pipeline, usaspending())
