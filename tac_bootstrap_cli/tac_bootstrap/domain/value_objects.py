"""
TAC Bootstrap Domain Value Objects

Type-safe value objects with automatic validation for critical domain concepts.
Value objects fail fast at construction time, preventing invalid data propagation.

These value objects inherit from str for compatibility with existing code and Pydantic v2
models, while providing strong validation guarantees through the __new__ method.

Example usage:
    from tac_bootstrap.domain.value_objects import (
        ProjectName,
        TemplatePath,
        SemanticVersion
    )

    # ProjectName - sanitizes to lowercase-hyphen format
    name = ProjectName("My App!!")  # Returns: "my-app"

    # TemplatePath - prevents directory traversal
    path = TemplatePath("templates/config.yml")  # Valid
    bad_path = TemplatePath("../../etc/passwd")  # Raises ValueError

    # SemanticVersion - parses and compares versions
    v1 = SemanticVersion("1.2.3")
    v2 = SemanticVersion("0.10.2")
    assert v1 > v2  # True
    assert v1.tuple == (1, 2, 3)  # True
"""

import re
from typing import Any


class ProjectName(str):
    """
    Project name value object with automatic sanitization.

    Sanitizes project names to a safe lowercase-hyphen format suitable for:
    - Directory names
    - Package names
    - Python module names
    - Git branch names

    Sanitization rules:
    - Strips whitespace
    - Converts to lowercase
    - Replaces spaces with hyphens
    - Removes all non-alphanumeric-hyphen characters
    - Collapses consecutive hyphens into single hyphen
    - Enforces 1-64 character length

    Examples:
        >>> ProjectName("My App!!")
        'my-app'
        >>> ProjectName("hello_world")
        'helloworld'
        >>> ProjectName("Project   Name")
        'project-name'
        >>> ProjectName("test--multiple---hyphens")
        'test-multiple-hyphens'

    Raises:
        ValueError: If sanitized name is empty or exceeds 64 characters
    """

    def __new__(cls, value: str) -> "ProjectName":
        """
        Create and validate a ProjectName instance.

        Args:
            value: Raw project name string to sanitize

        Returns:
            Sanitized ProjectName instance

        Raises:
            ValueError: If sanitized name is empty or too long
        """
        if not isinstance(value, str):
            raise ValueError(f"Project name must be a string, got {type(value).__name__}")

        # Sanitize: strip, lowercase, replace spaces with hyphens
        sanitized = value.strip().lower().replace(" ", "-")

        # Remove all non-alphanumeric-hyphen characters
        sanitized = re.sub(r"[^a-z0-9-]", "", sanitized)

        # Collapse consecutive hyphens into single hyphen
        sanitized = re.sub(r"-+", "-", sanitized)

        # Remove leading/trailing hyphens
        sanitized = sanitized.strip("-")

        # Validate result
        if not sanitized:
            raise ValueError(
                f"Project name '{value}' cannot be empty after sanitization. "
                "Must contain at least one alphanumeric character."
            )

        if len(sanitized) > 64:
            raise ValueError(
                f"Project name '{sanitized}' exceeds maximum length of 64 characters "
                f"(got {len(sanitized)} characters)"
            )

        return str.__new__(cls, sanitized)


class TemplatePath(str):
    """
    Template path value object with security validation.

    Validates relative paths to template files, preventing directory traversal attacks
    and other path-based security vulnerabilities. This is critical for a code generator
    that reads template files and copies them to target directories.

    Validation rules:
    - Must be a relative path (no leading /)
    - Cannot contain parent directory traversal (..)
    - Cannot be empty
    - Allows dot-relative paths (./file)

    Security rationale:
    - Prevents reading arbitrary files outside template directory
    - Prevents writing to arbitrary locations
    - Protects against path traversal exploits

    Examples:
        >>> TemplatePath("templates/config.yml")
        'templates/config.yml'
        >>> TemplatePath("./templates/file.md")
        './templates/file.md'
        >>> TemplatePath("/etc/passwd")
        Traceback (most recent call last):
            ...
        ValueError: Absolute paths are not allowed...
        >>> TemplatePath("../../secret")
        Traceback (most recent call last):
            ...
        ValueError: Parent directory traversal (..) is not allowed...

    Raises:
        ValueError: If path is absolute, contains .., or is empty
    """

    def __new__(cls, value: str) -> "TemplatePath":
        """
        Create and validate a TemplatePath instance.

        Args:
            value: Relative path string to validate

        Returns:
            Validated TemplatePath instance

        Raises:
            ValueError: If path is absolute, contains .., or is empty
        """
        if not isinstance(value, str):
            raise ValueError(f"Template path must be a string, got {type(value).__name__}")

        # Validate not empty
        if not value or not value.strip():
            raise ValueError("Template path cannot be empty")

        # Validate not absolute path
        if value.startswith("/"):
            raise ValueError(
                f"Absolute paths are not allowed for security reasons. "
                f"Got: '{value}'. Use relative paths like 'templates/file.yml'"
            )

        # Validate no parent directory traversal
        if ".." in value:
            raise ValueError(
                f"Parent directory traversal (..) is not allowed for security reasons. "
                f"Got: '{value}'. This prevents path traversal attacks."
            )

        return str.__new__(cls, value)


class SemanticVersion(str):
    """
    Semantic version value object with parsing and comparison.

    Parses and validates semantic versions in strict X.Y.Z format where X, Y, Z are
    non-negative integers. Provides comparison operators and tuple representation.

    Format: MAJOR.MINOR.PATCH
    - MAJOR: Breaking changes
    - MINOR: New features (backwards compatible)
    - PATCH: Bug fixes (backwards compatible)

    Comparison follows semantic versioning rules:
    - 1.0.0 > 0.10.2
    - 0.10.2 > 0.2.0
    - 1.2.3 == 1.2.3

    Use cases:
    - TAC Bootstrap version comparison for upgrade detection
    - Template compatibility checking
    - Dependency version requirements

    Examples:
        >>> v1 = SemanticVersion("1.2.3")
        >>> v1.tuple
        (1, 2, 3)
        >>> v2 = SemanticVersion("0.10.2")
        >>> v1 > v2
        True
        >>> SemanticVersion("1.2")
        Traceback (most recent call last):
            ...
        ValueError: Invalid semantic version format...

    Raises:
        ValueError: If version doesn't match X.Y.Z format with integers
    """

    _tuple: tuple[int, int, int]

    def __new__(cls, value: str) -> "SemanticVersion":
        """
        Create and validate a SemanticVersion instance.

        Args:
            value: Version string in X.Y.Z format

        Returns:
            Validated SemanticVersion instance

        Raises:
            ValueError: If format is invalid
        """
        if not isinstance(value, str):
            raise ValueError(f"Semantic version must be a string, got {type(value).__name__}")

        # Validate format: X.Y.Z where X, Y, Z are integers
        pattern = r"^(\d+)\.(\d+)\.(\d+)$"
        match = re.match(pattern, value)

        if not match:
            raise ValueError(
                f"Invalid semantic version format: '{value}'. "
                "Expected format: X.Y.Z where X, Y, Z are non-negative integers. "
                "Examples: '1.2.3', '0.1.0', '10.0.5'"
            )

        # Create instance and store parsed tuple
        instance = str.__new__(cls, value)
        # Store parsed tuple as private attribute
        instance._tuple = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return instance

    @property
    def tuple(self) -> tuple[int, int, int]:
        """
        Get version as tuple of (major, minor, patch).

        Returns:
            Tuple of three integers representing major, minor, patch versions

        Example:
            >>> SemanticVersion("1.2.3").tuple
            (1, 2, 3)
        """
        return self._tuple

    def __eq__(self, other: Any) -> bool:
        """Compare versions for equality."""
        if not isinstance(other, (SemanticVersion, str)):
            return NotImplemented
        if isinstance(other, str):
            try:
                other = SemanticVersion(other)
            except ValueError:
                return False
        # At this point, other is guaranteed to be SemanticVersion
        assert isinstance(other, SemanticVersion)
        return self.tuple == other.tuple

    def __ne__(self, other: Any) -> bool:
        """Compare versions for inequality."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other: Any) -> bool:
        """Compare if this version is less than other."""
        if not isinstance(other, (SemanticVersion, str)):
            return NotImplemented
        if isinstance(other, str):
            try:
                other = SemanticVersion(other)
            except ValueError:
                return NotImplemented
        # At this point, other is guaranteed to be SemanticVersion
        assert isinstance(other, SemanticVersion)
        return self.tuple < other.tuple

    def __le__(self, other: Any) -> bool:
        """Compare if this version is less than or equal to other."""
        if not isinstance(other, (SemanticVersion, str)):
            return NotImplemented
        if isinstance(other, str):
            try:
                other = SemanticVersion(other)
            except ValueError:
                return NotImplemented
        # At this point, other is guaranteed to be SemanticVersion
        assert isinstance(other, SemanticVersion)
        return self.tuple <= other.tuple

    def __gt__(self, other: Any) -> bool:
        """Compare if this version is greater than other."""
        if not isinstance(other, (SemanticVersion, str)):
            return NotImplemented
        if isinstance(other, str):
            try:
                other = SemanticVersion(other)
            except ValueError:
                return NotImplemented
        # At this point, other is guaranteed to be SemanticVersion
        assert isinstance(other, SemanticVersion)
        return self.tuple > other.tuple

    def __ge__(self, other: Any) -> bool:
        """Compare if this version is greater than or equal to other."""
        if not isinstance(other, (SemanticVersion, str)):
            return NotImplemented
        if isinstance(other, str):
            try:
                other = SemanticVersion(other)
            except ValueError:
                return NotImplemented
        # At this point, other is guaranteed to be SemanticVersion
        assert isinstance(other, SemanticVersion)
        return self.tuple >= other.tuple

    def __hash__(self) -> int:
        """
        Return hash for use in sets and dicts.

        Returns:
            Hash of the version tuple

        Example:
            >>> v1 = SemanticVersion("1.2.3")
            >>> v2 = SemanticVersion("1.2.3")
            >>> {v1, v2}
            {SemanticVersion('1.2.3')}
        """
        return hash(self.tuple)
