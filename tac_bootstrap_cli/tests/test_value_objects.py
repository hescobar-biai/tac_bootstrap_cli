"""
Tests for TAC Bootstrap domain value objects.

Comprehensive test coverage for ProjectName, TemplatePath, and SemanticVersion
value objects, ensuring validation, sanitization, and comparison logic works correctly.
"""

import pytest

from tac_bootstrap.domain.value_objects import ProjectName, SemanticVersion, TemplatePath

# ============================================================================
# ProjectName Tests
# ============================================================================


class TestProjectName:
    """Tests for ProjectName value object."""

    def test_simple_sanitization(self):
        """Test basic sanitization of project name."""
        assert ProjectName("My App!!") == "my-app"
        assert ProjectName("Hello World") == "hello-world"
        assert ProjectName("TEST_PROJECT") == "testproject"

    def test_space_to_hyphen_conversion(self):
        """Test that spaces are converted to hyphens."""
        assert ProjectName("my project") == "my-project"
        assert ProjectName("  multi   space   test  ") == "multi-space-test"
        assert ProjectName("Project Name") == "project-name"

    def test_special_character_removal(self):
        """Test that special characters are removed."""
        assert ProjectName("my@app#test!") == "myapptest"
        assert ProjectName("app_with_underscores") == "appwithunderscores"
        assert ProjectName("email@domain.com") == "emaildomaincom"
        assert ProjectName("v1.2.3") == "v123"

    def test_consecutive_hyphen_collapsing(self):
        """Test that consecutive hyphens are collapsed into single hyphen."""
        assert ProjectName("my--app") == "my-app"
        assert ProjectName("test---multiple----hyphens") == "test-multiple-hyphens"
        assert ProjectName("a--b--c") == "a-b-c"

    def test_leading_trailing_hyphen_removal(self):
        """Test that leading and trailing hyphens are removed."""
        assert ProjectName("-my-app-") == "my-app"
        assert ProjectName("---test---") == "test"
        assert ProjectName("-a-b-c-") == "a-b-c"

    def test_empty_string_rejection(self):
        """Test that empty strings are rejected."""
        with pytest.raises(ValueError, match="cannot be empty after sanitization"):
            ProjectName("")

    def test_whitespace_only_rejection(self):
        """Test that whitespace-only strings are rejected."""
        with pytest.raises(ValueError, match="cannot be empty after sanitization"):
            ProjectName("   ")

    def test_special_chars_only_rejection(self):
        """Test that strings with only special characters are rejected."""
        with pytest.raises(ValueError, match="cannot be empty after sanitization"):
            ProjectName("!@#$%^&*()")

    def test_maximum_length_enforcement(self):
        """Test that names exceeding 64 characters are rejected."""
        # 65 characters (exceeds limit)
        long_name = "a" * 65
        with pytest.raises(ValueError, match="exceeds maximum length of 64 characters"):
            ProjectName(long_name)

    def test_maximum_length_boundary(self):
        """Test that exactly 64 characters is allowed."""
        # Exactly 64 characters (should pass)
        max_name = "a" * 64
        assert ProjectName(max_name) == max_name

    def test_numbers_allowed(self):
        """Test that numbers are preserved in project names."""
        assert ProjectName("app123") == "app123"
        assert ProjectName("v2") == "v2"
        assert ProjectName("test-v1-alpha2") == "test-v1-alpha2"

    def test_single_character(self):
        """Test single character names."""
        assert ProjectName("a") == "a"
        assert ProjectName("Z") == "z"
        assert ProjectName("5") == "5"

    def test_all_hyphens_rejected(self):
        """Test that strings with only hyphens are rejected."""
        with pytest.raises(ValueError, match="cannot be empty after sanitization"):
            ProjectName("---")

    def test_non_string_type_rejection(self):
        """Test that non-string types are rejected."""
        with pytest.raises(ValueError, match="must be a string"):
            ProjectName(123)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="must be a string"):
            ProjectName(None)  # type: ignore[arg-type]

    def test_lowercase_conversion(self):
        """Test that uppercase is converted to lowercase."""
        assert ProjectName("UPPERCASE") == "uppercase"
        assert ProjectName("MixedCase") == "mixedcase"
        assert ProjectName("CamelCase") == "camelcase"

    def test_complex_sanitization(self):
        """Test complex real-world project names."""
        assert ProjectName("My Awesome App v2.0!!") == "my-awesome-app-v20"
        assert ProjectName("  @company/package-name  ") == "companypackage-name"
        assert ProjectName("Test___Multiple___Underscores") == "testmultipleunderscores"

    def test_isinstance_str(self):
        """Test that ProjectName is a string subclass."""
        name = ProjectName("test")
        assert isinstance(name, str)
        assert isinstance(name, ProjectName)


# ============================================================================
# TemplatePath Tests
# ============================================================================


class TestTemplatePath:
    """Tests for TemplatePath value object."""

    def test_valid_relative_paths(self):
        """Test that valid relative paths are accepted."""
        assert TemplatePath("templates/config.yml") == "templates/config.yml"
        assert TemplatePath("path/to/file.md") == "path/to/file.md"
        assert TemplatePath("file.txt") == "file.txt"

    def test_valid_dot_relative_paths(self):
        """Test that dot-relative paths are accepted."""
        assert TemplatePath("./templates/file") == "./templates/file"
        assert TemplatePath("./file.txt") == "./file.txt"

    def test_reject_absolute_paths(self):
        """Test that absolute paths are rejected."""
        with pytest.raises(ValueError, match="Absolute paths are not allowed"):
            TemplatePath("/etc/passwd")
        with pytest.raises(ValueError, match="Absolute paths are not allowed"):
            TemplatePath("/root/secret")
        with pytest.raises(ValueError, match="Absolute paths are not allowed"):
            TemplatePath("/tmp/file")

    def test_reject_parent_traversal(self):
        """Test that parent directory traversal is rejected."""
        with pytest.raises(ValueError, match="Parent directory traversal"):
            TemplatePath("../../../etc/passwd")
        with pytest.raises(ValueError, match="Parent directory traversal"):
            TemplatePath("..")
        with pytest.raises(ValueError, match="Parent directory traversal"):
            TemplatePath("../..")

    def test_reject_embedded_traversal(self):
        """Test that embedded parent traversal is rejected."""
        with pytest.raises(ValueError, match="Parent directory traversal"):
            TemplatePath("templates/../../secret")
        with pytest.raises(ValueError, match="Parent directory traversal"):
            TemplatePath("path/../../../etc/passwd")

    def test_reject_empty_paths(self):
        """Test that empty paths are rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            TemplatePath("")

    def test_reject_whitespace_only_paths(self):
        """Test that whitespace-only paths are rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            TemplatePath("   ")

    def test_paths_with_dots_in_filenames(self):
        """Test that paths with dots in filenames (not ..) are accepted."""
        assert TemplatePath("file.config.yml") == "file.config.yml"
        assert TemplatePath("templates/app.v2.conf") == "templates/app.v2.conf"
        assert TemplatePath(".gitignore") == ".gitignore"
        assert TemplatePath("path/.hidden/file") == "path/.hidden/file"

    def test_non_string_type_rejection(self):
        """Test that non-string types are rejected."""
        with pytest.raises(ValueError, match="must be a string"):
            TemplatePath(123)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="must be a string"):
            TemplatePath(None)  # type: ignore[arg-type]

    def test_complex_valid_paths(self):
        """Test complex but valid template paths."""
        assert TemplatePath("a/b/c/d/e/file.txt") == "a/b/c/d/e/file.txt"
        assert TemplatePath("templates/python/fastapi/config.yml") == (
            "templates/python/fastapi/config.yml"
        )

    def test_isinstance_str(self):
        """Test that TemplatePath is a string subclass."""
        path = TemplatePath("templates/file")
        assert isinstance(path, str)
        assert isinstance(path, TemplatePath)


# ============================================================================
# SemanticVersion Tests
# ============================================================================


class TestSemanticVersion:
    """Tests for SemanticVersion value object."""

    def test_valid_parsing(self):
        """Test that valid semantic versions are parsed correctly."""
        assert SemanticVersion("1.2.3") == "1.2.3"
        assert SemanticVersion("0.0.0") == "0.0.0"
        assert SemanticVersion("10.20.30") == "10.20.30"

    def test_tuple_property(self):
        """Test that tuple property returns correct values."""
        v1 = SemanticVersion("1.2.3")
        assert v1.tuple == (1, 2, 3)

        v2 = SemanticVersion("0.0.0")
        assert v2.tuple == (0, 0, 0)

        v3 = SemanticVersion("100.200.300")
        assert v3.tuple == (100, 200, 300)

    def test_equality_comparison(self):
        """Test equality comparison between versions."""
        v1 = SemanticVersion("1.2.3")
        v2 = SemanticVersion("1.2.3")
        v3 = SemanticVersion("1.2.4")

        assert v1 == v2
        assert not (v1 == v3)
        assert v1 != v3
        assert not (v1 != v2)

    def test_equality_with_string(self):
        """Test equality comparison with string."""
        v1 = SemanticVersion("1.2.3")
        assert v1 == "1.2.3"
        assert not (v1 == "1.2.4")

    def test_less_than_comparison(self):
        """Test less than comparison."""
        assert SemanticVersion("1.0.0") < SemanticVersion("2.0.0")
        assert SemanticVersion("1.2.3") < SemanticVersion("1.2.4")
        assert SemanticVersion("0.2.0") < SemanticVersion("0.9.9")
        assert not (SemanticVersion("1.2.3") < SemanticVersion("1.2.3"))

    def test_less_than_with_string(self):
        """Test less than comparison with string."""
        v1 = SemanticVersion("0.6.0")
        assert v1 < "0.9.9"
        assert not (v1 < "0.1.0")

    def test_less_than_or_equal_comparison(self):
        """Test less than or equal comparison."""
        assert SemanticVersion("0.9.9") <= SemanticVersion("0.9.9")
        assert SemanticVersion("1.2.3") <= SemanticVersion("1.2.3")
        assert not (SemanticVersion("2.0.0") <= SemanticVersion("1.0.0"))

    def test_greater_than_comparison(self):
        """Test greater than comparison."""
        assert SemanticVersion("0.9.9") > SemanticVersion("0.2.0")
        assert SemanticVersion("2.0.0") > SemanticVersion("1.0.0")
        assert SemanticVersion("1.2.4") > SemanticVersion("1.2.3")
        assert not (SemanticVersion("1.2.3") > SemanticVersion("1.2.3"))

    def test_greater_than_with_string(self):
        """Test greater than comparison with string."""
        v1 = SemanticVersion("0.9.9")
        assert v1 > "0.2.0"
        assert not (v1 > "1.0.0")

    def test_greater_than_or_equal_comparison(self):
        """Test greater than or equal comparison."""
        assert SemanticVersion("0.9.9") >= SemanticVersion("0.9.9")
        assert SemanticVersion("1.2.3") >= SemanticVersion("1.2.3")
        assert not (SemanticVersion("1.0.0") >= SemanticVersion("2.0.0"))

    def test_comparison_major_version(self):
        """Test that major version takes precedence in comparison."""
        assert SemanticVersion("2.0.0") > SemanticVersion("1.9.9")
        assert SemanticVersion("1.0.0") > SemanticVersion("0.9.9")

    def test_comparison_minor_version(self):
        """Test that minor version is considered when major is equal."""
        assert SemanticVersion("1.3.0") > SemanticVersion("1.2.9")
        assert SemanticVersion("0.9.9") > SemanticVersion("0.2.9")

    def test_comparison_patch_version(self):
        """Test that patch version is considered when major and minor are equal."""
        assert SemanticVersion("1.2.4") > SemanticVersion("1.2.3")
        assert SemanticVersion("0.0.2") > SemanticVersion("0.0.1")

    def test_hash_consistency(self):
        """Test that hash is consistent for use in sets/dicts."""
        v1 = SemanticVersion("1.2.3")
        v2 = SemanticVersion("1.2.3")
        v3 = SemanticVersion("1.2.4")

        # Same version should have same hash
        assert hash(v1) == hash(v2)

        # Can be used in sets
        version_set = {v1, v2, v3}
        assert len(version_set) == 2  # v1 and v2 are duplicate

        # Can be used as dict keys
        version_dict = {v1: "a", v2: "b", v3: "c"}
        assert len(version_dict) == 2  # v1 and v2 are same key
        assert version_dict[v1] == "b"  # v2 overwrote v1

    def test_invalid_format_rejection(self):
        """Test that invalid version formats are rejected."""
        # Too few components
        with pytest.raises(ValueError, match="Invalid semantic version format"):
            SemanticVersion("1.2")
        with pytest.raises(ValueError, match="Invalid semantic version format"):
            SemanticVersion("1")

        # Too many components
        with pytest.raises(ValueError, match="Invalid semantic version format"):
            SemanticVersion("1.2.3.4")

        # Non-numeric components
        with pytest.raises(ValueError, match="Invalid semantic version format"):
            SemanticVersion("1.2.x")
        with pytest.raises(ValueError, match="Invalid semantic version format"):
            SemanticVersion("abc")

        # Prefix/suffix
        with pytest.raises(ValueError, match="Invalid semantic version format"):
            SemanticVersion("v1.2.3")
        with pytest.raises(ValueError, match="Invalid semantic version format"):
            SemanticVersion("1.2.3-alpha")

    def test_edge_case_zero_version(self):
        """Test edge case of version 0.0.0."""
        v = SemanticVersion("0.0.0")
        assert v.tuple == (0, 0, 0)
        assert v == "0.0.0"

    def test_edge_case_large_numbers(self):
        """Test edge case with large version numbers."""
        v = SemanticVersion("999.888.777")
        assert v.tuple == (999, 888, 777)
        assert v > "1.0.0"

    def test_non_string_type_rejection(self):
        """Test that non-string types are rejected."""
        with pytest.raises(ValueError, match="must be a string"):
            SemanticVersion(123)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="must be a string"):
            SemanticVersion(None)  # type: ignore[arg-type]

    def test_isinstance_str(self):
        """Test that SemanticVersion is a string subclass."""
        version = SemanticVersion("1.2.3")
        assert isinstance(version, str)
        assert isinstance(version, SemanticVersion)

    def test_sorting(self):
        """Test that versions can be sorted correctly."""
        versions = [
            SemanticVersion("1.0.0"),
            SemanticVersion("0.9.9"),
            SemanticVersion("0.9.9"),
            SemanticVersion("1.2.3"),
            SemanticVersion("0.1.0"),
        ]
        sorted_versions = sorted(versions)
        assert sorted_versions == [
            SemanticVersion("0.1.0"),
            SemanticVersion("0.9.9"),
            SemanticVersion("0.9.9"),
            SemanticVersion("1.0.0"),
            SemanticVersion("1.2.3"),
        ]

    def test_comparison_with_invalid_types(self):
        """Test comparison with incompatible types."""
        v = SemanticVersion("1.2.3")
        # Equality returns False for incompatible types
        assert (v == 123) is False
        # Ordering comparisons raise TypeError for incompatible types
        with pytest.raises(TypeError):
            v < 123  # type: ignore[operator]

    def test_comparison_with_invalid_string(self):
        """Test comparison with invalid version string."""
        v = SemanticVersion("1.2.3")
        # Comparing with invalid version string
        assert (v == "invalid") is False
