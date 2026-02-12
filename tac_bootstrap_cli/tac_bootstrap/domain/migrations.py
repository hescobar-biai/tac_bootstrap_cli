"""
TAC Bootstrap Schema Migration Definitions

Defines the migration registry and transformation functions for upgrading
(and rolling back) config.yml schemas between versions.

Each migration is a pair of forward/backward callables that transform
a raw config dictionary from one schema version to the next.

Example usage:
    from tac_bootstrap.domain.migrations import MIGRATION_REGISTRY, get_latest_version

    migration = MIGRATION_REGISTRY["1->2"]
    new_config = migration.forward(old_config)

    latest = get_latest_version()  # "2"
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Dict, List

from tac_bootstrap import __version__

# ============================================================================
# MIGRATION DATA CLASS
# ============================================================================


@dataclass(frozen=True)
class Migration:
    """
    Represents a single schema migration between two versions.

    Attributes:
        version_from: Source schema version string (e.g., "1").
        version_to: Target schema version string (e.g., "2").
        description: Human-readable description of the migration.
        forward: Callable that transforms config dict from version_from to version_to.
        backward: Callable that transforms config dict from version_to to version_from.
    """

    version_from: str
    version_to: str
    description: str
    forward: Callable[[dict], dict]
    backward: Callable[[dict], dict]


# ============================================================================
# MIGRATION FUNCTIONS: v1 -> v2
# ============================================================================


def migrate_v1_to_v2(config: dict) -> dict:
    """
    Migrate config from schema v1 to v2.

    Changes:
        - Sets schema_version to 2.
        - Adds metadata block with generated_at, generated_by,
          last_upgrade, schema_version, and template_checksums.

    Args:
        config: Raw config dictionary at schema v1.

    Returns:
        Transformed config dictionary at schema v2.
    """
    now_iso = datetime.now(timezone.utc).isoformat()

    # Update schema_version
    config["schema_version"] = 2

    # Add metadata section
    if "metadata" not in config or config["metadata"] is None:
        config["metadata"] = {
            "generated_at": config.get("_generated_at", now_iso),
            "generated_by": f"tac-bootstrap v{__version__}",
            "last_upgrade": now_iso,
            "schema_version": 2,
            "template_checksums": {},
        }
    else:
        # Metadata already exists (partial migration); update relevant fields
        config["metadata"]["last_upgrade"] = now_iso
        config["metadata"]["schema_version"] = 2
        if "generated_by" not in config["metadata"]:
            config["metadata"]["generated_by"] = f"tac-bootstrap v{__version__}"
        if "generated_at" not in config["metadata"]:
            config["metadata"]["generated_at"] = now_iso
        if "template_checksums" not in config["metadata"]:
            config["metadata"]["template_checksums"] = {}

    # Clean up internal helper key if present
    config.pop("_generated_at", None)

    return config


def migrate_v2_to_v1(config: dict) -> dict:
    """
    Rollback config from schema v2 to v1.

    Changes:
        - Sets schema_version back to 1.
        - Removes the metadata block entirely.

    Args:
        config: Raw config dictionary at schema v2.

    Returns:
        Transformed config dictionary at schema v1.
    """
    config["schema_version"] = 1

    # Remove metadata section
    config.pop("metadata", None)

    return config


# ============================================================================
# MIGRATION FUNCTIONS: v2 -> v3
# ============================================================================


def migrate_v2_to_v3(config: dict) -> dict:
    """
    Migrate config from schema v2 to v3.

    Changes:
        - Sets schema_version to 3.
        - Adds optional data_engineering, ml, and infrastructure sections (null by default).

    Args:
        config: Raw config dictionary at schema v2.

    Returns:
        Transformed config dictionary at schema v3.
    """
    now_iso = datetime.now(timezone.utc).isoformat()

    config["schema_version"] = 3

    # Add optional Celes stack sections (null = disabled)
    if "data_engineering" not in config:
        config["data_engineering"] = None
    if "ml" not in config:
        config["ml"] = None
    if "infrastructure" not in config:
        config["infrastructure"] = None

    # Update metadata
    if config.get("metadata"):
        config["metadata"]["last_upgrade"] = now_iso
        config["metadata"]["schema_version"] = 3

    return config


def migrate_v3_to_v2(config: dict) -> dict:
    """
    Rollback config from schema v3 to v2.

    Changes:
        - Sets schema_version back to 2.
        - Removes data_engineering, ml, and infrastructure sections.

    Args:
        config: Raw config dictionary at schema v3.

    Returns:
        Transformed config dictionary at schema v2.
    """
    config["schema_version"] = 2

    config.pop("data_engineering", None)
    config.pop("ml", None)
    config.pop("infrastructure", None)

    # Update metadata
    if config.get("metadata"):
        config["metadata"]["schema_version"] = 2

    return config


# ============================================================================
# MIGRATION REGISTRY
# ============================================================================


MIGRATION_REGISTRY: Dict[str, Migration] = {
    "1->2": Migration(
        version_from="1",
        version_to="2",
        description="Add schema_version=2 and metadata fields (generated_at, generated_by, "
        "last_upgrade, template_checksums)",
        forward=migrate_v1_to_v2,
        backward=migrate_v2_to_v1,
    ),
    "2->3": Migration(
        version_from="2",
        version_to="3",
        description="Add optional data_engineering, ml, and infrastructure config sections "
        "for Celes stack support",
        forward=migrate_v2_to_v3,
        backward=migrate_v3_to_v2,
    ),
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_latest_version() -> str:
    """
    Determine the latest schema version from the migration registry.

    Scans all registered migrations and returns the highest version_to value.
    Falls back to "1" if the registry is empty.

    Returns:
        The latest schema version string (e.g., "2").
    """
    if not MIGRATION_REGISTRY:
        return "1"

    all_versions: List[int] = []
    for migration in MIGRATION_REGISTRY.values():
        all_versions.append(int(migration.version_from))
        all_versions.append(int(migration.version_to))

    return str(max(all_versions))


def get_migration_path(from_version: str, to_version: str) -> List[Migration]:
    """
    Find the ordered list of migrations needed to go from one version to another.

    Supports both forward (upgrade) and backward (rollback) migration paths.
    For forward migrations, the path is built by chaining version_from -> version_to.
    For backward migrations, the path is built in reverse using backward callables.

    Args:
        from_version: Current schema version string.
        to_version: Target schema version string.

    Returns:
        Ordered list of Migration objects forming the path.

    Raises:
        ValueError: If no migration path exists between the given versions.
    """
    from_int = int(from_version)
    to_int = int(to_version)

    if from_int == to_int:
        return []

    migrations: List[Migration] = []

    if from_int < to_int:
        # Forward migration path
        current = from_int
        while current < to_int:
            key = f"{current}->{current + 1}"
            if key not in MIGRATION_REGISTRY:
                raise ValueError(
                    f"No migration path found from version {from_version} to {to_version}. "
                    f"Missing migration: {key}"
                )
            migrations.append(MIGRATION_REGISTRY[key])
            current += 1
    else:
        # Backward migration path (rollback)
        current = from_int
        while current > to_int:
            key = f"{current - 1}->{current}"
            if key not in MIGRATION_REGISTRY:
                raise ValueError(
                    f"No rollback path found from version {from_version} to {to_version}. "
                    f"Missing migration: {key}"
                )
            migrations.append(MIGRATION_REGISTRY[key])
            current -= 1

    return migrations
