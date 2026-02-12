"""
BigQuery Data Loader

Loads data files from Google Cloud Storage into BigQuery with:
- Cloud Storage file discovery (prefix-based and glob patterns)
- Schema auto-detection with optional explicit schema override
- Configurable load job settings (format, write disposition, partitioning)
- Retry logic with exponential backoff
- Comprehensive error handling and logging

Usage:
    python loader.py \
        --bucket my-data-bucket \
        --prefix raw/events/dt=2025-01-15/ \
        --dataset analytics \
        --table raw_events \
        --format PARQUET

    python loader.py \
        --bucket my-data-bucket \
        --prefix raw/sales/ \
        --dataset analytics \
        --table raw_sales \
        --format CSV \
        --write-disposition WRITE_TRUNCATE \
        --partition-field sale_date \
        --cluster-fields region,product_category \
        --skip-leading-rows 1

    python loader.py \
        --bucket my-data-bucket \
        --prefix raw/events/ \
        --dataset analytics \
        --table raw_events \
        --format PARQUET \
        --schema-file schema.json \
        --partition-field event_date \
        --partition-type DAY \
        --max-retries 5
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Optional

from google.api_core import exceptions as gcp_exceptions
from google.api_core import retry as gcp_retry
from google.cloud import bigquery, storage

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SOURCE_FORMAT_MAP = {
    "CSV": bigquery.SourceFormat.CSV,
    "JSON": bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    "NEWLINE_DELIMITED_JSON": bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    "AVRO": bigquery.SourceFormat.AVRO,
    "PARQUET": bigquery.SourceFormat.PARQUET,
    "ORC": bigquery.SourceFormat.ORC,
}

WRITE_DISPOSITION_MAP = {
    "WRITE_TRUNCATE": bigquery.WriteDisposition.WRITE_TRUNCATE,
    "WRITE_APPEND": bigquery.WriteDisposition.WRITE_APPEND,
    "WRITE_EMPTY": bigquery.WriteDisposition.WRITE_EMPTY,
}

PARTITION_TYPE_MAP = {
    "DAY": bigquery.TimePartitioningType.DAY,
    "HOUR": bigquery.TimePartitioningType.HOUR,
    "MONTH": bigquery.TimePartitioningType.MONTH,
    "YEAR": bigquery.TimePartitioningType.YEAR,
}

DEFAULT_MAX_RETRIES = 3
DEFAULT_INITIAL_BACKOFF_SECONDS = 2.0
DEFAULT_BACKOFF_MULTIPLIER = 2.0
DEFAULT_MAX_BACKOFF_SECONDS = 120.0


# ---------------------------------------------------------------------------
# File Discovery
# ---------------------------------------------------------------------------


def discover_files(
    bucket_name: str,
    prefix: str,
    file_extensions: Optional[list[str]] = None,
) -> list[str]:
    """Discover files in a Cloud Storage bucket matching a prefix.

    Lists all objects under the given prefix and optionally filters by file
    extension. Returns fully qualified GCS URIs.

    Args:
        bucket_name: Name of the GCS bucket (without gs:// prefix).
        prefix: Object prefix to search under (e.g., "raw/events/dt=2025-01-15/").
        file_extensions: Optional list of file extensions to include
            (e.g., [".parquet", ".csv"]). If None, all files are included.

    Returns:
        List of GCS URIs (e.g., ["gs://bucket/path/file.parquet"]).

    Raises:
        ValueError: If no files are found matching the criteria.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=prefix))

    uris: list[str] = []
    for blob in blobs:
        # Skip directory markers (zero-byte objects ending with /)
        if blob.name.endswith("/") and blob.size == 0:
            continue

        # Filter by extension if specified
        if file_extensions:
            if not any(blob.name.lower().endswith(ext.lower()) for ext in file_extensions):
                continue

        uris.append(f"gs://{bucket_name}/{blob.name}")

    if not uris:
        raise ValueError(
            f"No files found in gs://{bucket_name}/{prefix} "
            f"(extensions filter: {file_extensions})"
        )

    logger.info(
        "Discovered %d file(s) in gs://%s/%s", len(uris), bucket_name, prefix
    )
    for uri in uris[:5]:
        logger.info("  %s", uri)
    if len(uris) > 5:
        logger.info("  ... and %d more", len(uris) - 5)

    return uris


# ---------------------------------------------------------------------------
# Schema Loading
# ---------------------------------------------------------------------------


def load_schema_from_file(schema_path: str) -> list[bigquery.SchemaField]:
    """Load a BigQuery schema from a JSON file.

    The JSON file should contain an array of schema field definitions:
    [
        {"name": "event_id", "type": "STRING", "mode": "REQUIRED"},
        {"name": "event_date", "type": "DATE", "mode": "NULLABLE"},
        {"name": "payload", "type": "JSON", "mode": "NULLABLE"}
    ]

    Args:
        schema_path: Path to the JSON schema file.

    Returns:
        List of BigQuery SchemaField objects.

    Raises:
        FileNotFoundError: If the schema file does not exist.
        json.JSONDecodeError: If the schema file contains invalid JSON.
    """
    path = Path(schema_path)
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with open(path) as f:
        schema_defs = json.load(f)

    schema_fields = []
    for field_def in schema_defs:
        schema_fields.append(
            bigquery.SchemaField(
                name=field_def["name"],
                field_type=field_def["type"],
                mode=field_def.get("mode", "NULLABLE"),
                description=field_def.get("description", ""),
            )
        )

    logger.info("Loaded schema with %d fields from %s", len(schema_fields), schema_path)
    return schema_fields


# ---------------------------------------------------------------------------
# Load Job Configuration
# ---------------------------------------------------------------------------


def build_load_config(
    source_format: str,
    write_disposition: str = "WRITE_TRUNCATE",
    schema_file: Optional[str] = None,
    autodetect: bool = True,
    partition_field: Optional[str] = None,
    partition_type: str = "DAY",
    partition_expiration_ms: Optional[int] = None,
    cluster_fields: Optional[list[str]] = None,
    skip_leading_rows: int = 0,
    max_bad_records: int = 0,
    ignore_unknown_values: bool = False,
) -> bigquery.LoadJobConfig:
    """Build a BigQuery LoadJobConfig with the specified parameters.

    Args:
        source_format: File format (CSV, JSON, PARQUET, AVRO, ORC).
        write_disposition: How to handle existing data
            (WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY).
        schema_file: Optional path to a JSON schema file. If provided,
            autodetect is disabled.
        autodetect: Whether to auto-detect schema. Ignored if schema_file
            is provided.
        partition_field: Column name to partition by. If None, no
            time partitioning is configured.
        partition_type: Partitioning granularity (DAY, HOUR, MONTH, YEAR).
        partition_expiration_ms: Optional partition expiration in milliseconds.
        cluster_fields: Optional list of column names to cluster by (max 4).
        skip_leading_rows: Number of header rows to skip (CSV only).
        max_bad_records: Maximum number of bad records to tolerate before
            failing the job.
        ignore_unknown_values: Whether to ignore extra values not in the schema.

    Returns:
        Configured BigQuery LoadJobConfig.

    Raises:
        ValueError: If source_format or write_disposition is invalid.
    """
    fmt = source_format.upper()
    if fmt not in SOURCE_FORMAT_MAP:
        raise ValueError(
            f"Unsupported source format: {source_format}. "
            f"Supported: {list(SOURCE_FORMAT_MAP.keys())}"
        )

    wd = write_disposition.upper()
    if wd not in WRITE_DISPOSITION_MAP:
        raise ValueError(
            f"Unsupported write disposition: {write_disposition}. "
            f"Supported: {list(WRITE_DISPOSITION_MAP.keys())}"
        )

    config = bigquery.LoadJobConfig(
        source_format=SOURCE_FORMAT_MAP[fmt],
        write_disposition=WRITE_DISPOSITION_MAP[wd],
        max_bad_records=max_bad_records,
        ignore_unknown_values=ignore_unknown_values,
    )

    # Schema: explicit file takes precedence over autodetect
    if schema_file:
        config.schema = load_schema_from_file(schema_file)
        config.autodetect = False
        logger.info("Using explicit schema from %s", schema_file)
    else:
        config.autodetect = autodetect
        if autodetect:
            logger.info("Using schema auto-detection")

    # CSV-specific options
    if fmt == "CSV" and skip_leading_rows > 0:
        config.skip_leading_rows = skip_leading_rows

    # Time partitioning
    if partition_field:
        pt = partition_type.upper()
        if pt not in PARTITION_TYPE_MAP:
            raise ValueError(
                f"Unsupported partition type: {partition_type}. "
                f"Supported: {list(PARTITION_TYPE_MAP.keys())}"
            )
        partitioning = bigquery.TimePartitioning(
            type_=PARTITION_TYPE_MAP[pt],
            field=partition_field,
        )
        if partition_expiration_ms is not None:
            partitioning.expiration_ms = partition_expiration_ms
        config.time_partitioning = partitioning
        logger.info(
            "Partitioning by '%s' (%s granularity)", partition_field, pt
        )

    # Clustering
    if cluster_fields:
        if len(cluster_fields) > 4:
            raise ValueError(
                f"BigQuery supports at most 4 cluster fields, got {len(cluster_fields)}"
            )
        config.clustering_fields = cluster_fields
        logger.info("Clustering by: %s", ", ".join(cluster_fields))

    return config


# ---------------------------------------------------------------------------
# Load Execution with Retry
# ---------------------------------------------------------------------------


def load_to_bigquery(
    source_uris: list[str],
    project: str,
    dataset: str,
    table: str,
    job_config: bigquery.LoadJobConfig,
    max_retries: int = DEFAULT_MAX_RETRIES,
    initial_backoff: float = DEFAULT_INITIAL_BACKOFF_SECONDS,
    backoff_multiplier: float = DEFAULT_BACKOFF_MULTIPLIER,
    max_backoff: float = DEFAULT_MAX_BACKOFF_SECONDS,
) -> bigquery.LoadJob:
    """Execute a BigQuery load job with retry logic.

    Retries on transient errors (rate limits, internal errors, service
    unavailable) with exponential backoff. Non-transient errors fail
    immediately.

    Args:
        source_uris: List of GCS URIs to load.
        project: GCP project ID.
        dataset: BigQuery dataset name.
        table: BigQuery table name.
        job_config: Configured LoadJobConfig.
        max_retries: Maximum number of retry attempts.
        initial_backoff: Initial backoff duration in seconds.
        backoff_multiplier: Multiplier applied to backoff after each retry.
        max_backoff: Maximum backoff duration in seconds.

    Returns:
        Completed BigQuery LoadJob.

    Raises:
        google.api_core.exceptions.GoogleAPICallError: If the load job fails
            after all retries are exhausted.
    """
    client = bigquery.Client(project=project)
    table_ref = f"{project}.{dataset}.{table}"
    backoff = initial_backoff

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(
                "Starting load job (attempt %d/%d): %d file(s) -> %s",
                attempt,
                max_retries,
                len(source_uris),
                table_ref,
            )

            load_job = client.load_table_from_uri(
                source_uris,
                table_ref,
                job_config=job_config,
            )

            # Wait for the job to complete
            load_job.result()

            # Log success metrics
            logger.info(
                "Load job completed successfully: %s",
                load_job.job_id,
            )
            logger.info(
                "  Output rows: %s",
                load_job.output_rows,
            )
            logger.info(
                "  Output bytes: %s",
                load_job.output_bytes,
            )
            logger.info(
                "  Destination: %s",
                table_ref,
            )

            return load_job

        except (
            gcp_exceptions.TooManyRequests,
            gcp_exceptions.InternalServerError,
            gcp_exceptions.ServiceUnavailable,
            gcp_exceptions.BadGateway,
        ) as exc:
            if attempt == max_retries:
                logger.error(
                    "Load job failed after %d attempts: %s", max_retries, exc
                )
                raise

            logger.warning(
                "Transient error on attempt %d/%d: %s. "
                "Retrying in %.1f seconds...",
                attempt,
                max_retries,
                exc,
                backoff,
            )
            time.sleep(backoff)
            backoff = min(backoff * backoff_multiplier, max_backoff)

        except gcp_exceptions.GoogleAPICallError as exc:
            # Non-transient errors: fail immediately
            logger.error("Load job failed with non-transient error: %s", exc)
            if hasattr(exc, "errors") and exc.errors:
                for error in exc.errors:
                    logger.error("  Error detail: %s", error)
            raise

    # This should not be reached, but guard against it
    raise RuntimeError(f"Load job failed after {max_retries} attempts")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Optional argument list. Defaults to sys.argv[1:].

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Load data from Cloud Storage into BigQuery",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Load Parquet files with auto-detected schema
  python loader.py --bucket my-bucket --prefix raw/events/ \\
      --dataset analytics --table raw_events --format PARQUET

  # Load CSV with explicit schema and partitioning
  python loader.py --bucket my-bucket --prefix raw/sales/ \\
      --dataset analytics --table raw_sales --format CSV \\
      --schema-file schema.json --partition-field sale_date \\
      --skip-leading-rows 1 --write-disposition WRITE_TRUNCATE
        """,
    )

    # Required arguments
    parser.add_argument(
        "--bucket",
        required=True,
        help="GCS bucket name (without gs:// prefix)",
    )
    parser.add_argument(
        "--prefix",
        required=True,
        help="GCS object prefix to search for files",
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="BigQuery dataset name",
    )
    parser.add_argument(
        "--table",
        required=True,
        help="BigQuery table name",
    )

    # Format and disposition
    parser.add_argument(
        "--format",
        dest="source_format",
        default="PARQUET",
        choices=list(SOURCE_FORMAT_MAP.keys()),
        help="Source file format (default: PARQUET)",
    )
    parser.add_argument(
        "--write-disposition",
        default="WRITE_TRUNCATE",
        choices=list(WRITE_DISPOSITION_MAP.keys()),
        help="Write disposition for the load job (default: WRITE_TRUNCATE)",
    )

    # Schema
    parser.add_argument(
        "--schema-file",
        default=None,
        help="Path to JSON schema file. Disables auto-detection when provided.",
    )
    parser.add_argument(
        "--no-autodetect",
        action="store_true",
        default=False,
        help="Disable schema auto-detection (requires --schema-file)",
    )

    # Partitioning
    parser.add_argument(
        "--partition-field",
        default=None,
        help="Column to partition by",
    )
    parser.add_argument(
        "--partition-type",
        default="DAY",
        choices=list(PARTITION_TYPE_MAP.keys()),
        help="Partition granularity (default: DAY)",
    )
    parser.add_argument(
        "--partition-expiration-days",
        type=int,
        default=None,
        help="Number of days before partitions expire",
    )

    # Clustering
    parser.add_argument(
        "--cluster-fields",
        default=None,
        help="Comma-separated list of columns to cluster by (max 4)",
    )

    # CSV options
    parser.add_argument(
        "--skip-leading-rows",
        type=int,
        default=0,
        help="Number of header rows to skip for CSV files (default: 0)",
    )

    # Error tolerance
    parser.add_argument(
        "--max-bad-records",
        type=int,
        default=0,
        help="Maximum number of bad records to tolerate (default: 0)",
    )
    parser.add_argument(
        "--ignore-unknown-values",
        action="store_true",
        default=False,
        help="Ignore extra values not represented in the table schema",
    )

    # Retry configuration
    parser.add_argument(
        "--max-retries",
        type=int,
        default=DEFAULT_MAX_RETRIES,
        help=f"Maximum retry attempts for transient errors (default: {DEFAULT_MAX_RETRIES})",
    )

    # GCP project
    parser.add_argument(
        "--project",
        default=None,
        help="GCP project ID. If not specified, uses the default project.",
    )

    # File extension filter
    parser.add_argument(
        "--extensions",
        default=None,
        help="Comma-separated list of file extensions to include (e.g., .parquet,.csv)",
    )

    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    """Main entry point for the BigQuery data loader.

    Discovers files in Cloud Storage, configures a load job, and executes
    it with retry logic.

    Args:
        argv: Optional argument list for testing. Defaults to sys.argv[1:].
    """
    args = parse_args(argv)

    # Resolve GCP project
    project = args.project
    if project is None:
        # Use the default project from the environment / gcloud config
        client = bigquery.Client()
        project = client.project
        logger.info("Using default GCP project: %s", project)

    # Parse comma-separated fields
    cluster_fields = None
    if args.cluster_fields:
        cluster_fields = [f.strip() for f in args.cluster_fields.split(",")]

    extensions = None
    if args.extensions:
        extensions = [e.strip() for e in args.extensions.split(",")]

    # Partition expiration
    partition_expiration_ms = None
    if args.partition_expiration_days is not None:
        partition_expiration_ms = args.partition_expiration_days * 24 * 60 * 60 * 1000

    # Step 1: Discover files
    logger.info("=" * 60)
    logger.info("BigQuery Data Loader")
    logger.info("=" * 60)
    logger.info("Source: gs://%s/%s", args.bucket, args.prefix)
    logger.info("Target: %s.%s.%s", project, args.dataset, args.table)
    logger.info("Format: %s", args.source_format)
    logger.info("Write Disposition: %s", args.write_disposition)
    logger.info("-" * 60)

    try:
        source_uris = discover_files(
            bucket_name=args.bucket,
            prefix=args.prefix,
            file_extensions=extensions,
        )
    except ValueError as exc:
        logger.error("File discovery failed: %s", exc)
        sys.exit(1)

    # Step 2: Build load configuration
    autodetect = not args.no_autodetect and args.schema_file is None
    job_config = build_load_config(
        source_format=args.source_format,
        write_disposition=args.write_disposition,
        schema_file=args.schema_file,
        autodetect=autodetect,
        partition_field=args.partition_field,
        partition_type=args.partition_type,
        partition_expiration_ms=partition_expiration_ms,
        cluster_fields=cluster_fields,
        skip_leading_rows=args.skip_leading_rows,
        max_bad_records=args.max_bad_records,
        ignore_unknown_values=args.ignore_unknown_values,
    )

    # Step 3: Execute load job with retry
    try:
        load_job = load_to_bigquery(
            source_uris=source_uris,
            project=project,
            dataset=args.dataset,
            table=args.table,
            job_config=job_config,
            max_retries=args.max_retries,
        )
    except Exception as exc:
        logger.error("Load job failed: %s", exc)
        sys.exit(1)

    # Step 4: Report results
    logger.info("=" * 60)
    logger.info("LOAD COMPLETE")
    logger.info("  Job ID:      %s", load_job.job_id)
    logger.info("  Output Rows: %s", load_job.output_rows)
    logger.info("  Output Size: %s bytes", load_job.output_bytes)
    logger.info("  Destination: %s.%s.%s", project, args.dataset, args.table)
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
