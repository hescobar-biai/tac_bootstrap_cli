"""
Unit tests for tac_bootstrap.domain.validators module.

Tests all validation functions and compatibility mappings to ensure proper
error detection and suggestion generation for invalid configuration combinations.
"""

from tac_bootstrap.domain.models import Architecture, Framework, Language, PackageManager
from tac_bootstrap.domain.validators import (
    ARCHITECTURES_REQUIRING_BASE_CLASSES,
    COMPATIBLE_FRAMEWORKS,
    COMPATIBLE_PACKAGE_MANAGERS,
    ValidationIssue,
    validate_architecture_framework,
    validate_framework_language,
    validate_package_manager_language,
)


class TestValidateFrameworkLanguage:
    """Tests for validate_framework_language function."""

    def test_valid_python_frameworks(self):
        """Test all valid Python frameworks return None."""
        valid_frameworks = [
            Framework.FASTAPI,
            Framework.DJANGO,
            Framework.FLASK,
            Framework.NONE,
        ]
        for framework in valid_frameworks:
            result = validate_framework_language(framework, Language.PYTHON)
            assert result is None, f"{framework.value} should be valid for Python"

    def test_valid_typescript_frameworks(self):
        """Test all valid TypeScript frameworks return None."""
        valid_frameworks = [
            Framework.NEXTJS,
            Framework.EXPRESS,
            Framework.NESTJS,
            Framework.REACT,
            Framework.VUE,
            Framework.NONE,
        ]
        for framework in valid_frameworks:
            result = validate_framework_language(framework, Language.TYPESCRIPT)
            assert result is None, f"{framework.value} should be valid for TypeScript"

    def test_valid_javascript_frameworks(self):
        """Test all valid JavaScript frameworks return None."""
        valid_frameworks = [
            Framework.NEXTJS,
            Framework.EXPRESS,
            Framework.REACT,
            Framework.VUE,
            Framework.NONE,
        ]
        for framework in valid_frameworks:
            result = validate_framework_language(framework, Language.JAVASCRIPT)
            assert result is None, f"{framework.value} should be valid for JavaScript"

    def test_valid_go_frameworks(self):
        """Test all valid Go frameworks return None."""
        valid_frameworks = [Framework.GIN, Framework.ECHO, Framework.NONE]
        for framework in valid_frameworks:
            result = validate_framework_language(framework, Language.GO)
            assert result is None, f"{framework.value} should be valid for Go"

    def test_valid_rust_frameworks(self):
        """Test all valid Rust frameworks return None."""
        valid_frameworks = [Framework.AXUM, Framework.ACTIX, Framework.NONE]
        for framework in valid_frameworks:
            result = validate_framework_language(framework, Language.RUST)
            assert result is None, f"{framework.value} should be valid for Rust"

    def test_valid_java_frameworks(self):
        """Test all valid Java frameworks return None."""
        valid_frameworks = [Framework.SPRING, Framework.NONE]
        for framework in valid_frameworks:
            result = validate_framework_language(framework, Language.JAVA)
            assert result is None, f"{framework.value} should be valid for Java"

    def test_invalid_fastapi_with_go(self):
        """Test FastAPI is invalid for Go."""
        result = validate_framework_language(Framework.FASTAPI, Language.GO)
        assert result is not None
        assert isinstance(result, ValidationIssue)
        assert result.field_name == "framework"
        assert result.invalid_value == "fastapi"
        assert "not compatible" in result.message.lower()
        assert result.suggestions is not None
        assert "gin" in result.suggestions
        assert "echo" in result.suggestions

    def test_invalid_gin_with_python(self):
        """Test Gin is invalid for Python."""
        result = validate_framework_language(Framework.GIN, Language.PYTHON)
        assert result is not None
        assert isinstance(result, ValidationIssue)
        assert result.field_name == "framework"
        assert result.invalid_value == "gin"
        assert "not compatible" in result.message.lower()
        assert result.suggestions is not None
        assert "fastapi" in result.suggestions
        assert "django" in result.suggestions
        assert "flask" in result.suggestions

    def test_invalid_nestjs_with_go(self):
        """Test NestJS is invalid for Go."""
        result = validate_framework_language(Framework.NESTJS, Language.GO)
        assert result is not None
        assert isinstance(result, ValidationIssue)
        assert result.field_name == "framework"
        assert result.invalid_value == "nestjs"
        assert result.suggestions is not None

    def test_invalid_spring_with_python(self):
        """Test Spring is invalid for Python."""
        result = validate_framework_language(Framework.SPRING, Language.PYTHON)
        assert result is not None
        assert isinstance(result, ValidationIssue)
        assert result.field_name == "framework"
        assert result.invalid_value == "spring"
        assert result.suggestions is not None

    def test_framework_none_valid_for_all_languages(self):
        """Test Framework.NONE is valid for all languages."""
        all_languages = [
            Language.PYTHON,
            Language.TYPESCRIPT,
            Language.JAVASCRIPT,
            Language.GO,
            Language.RUST,
            Language.JAVA,
        ]
        for language in all_languages:
            result = validate_framework_language(Framework.NONE, language)
            assert result is None, f"Framework.NONE should be valid for {language.value}"

    def test_suggestions_are_populated(self):
        """Test that invalid combinations include suggestions."""
        result = validate_framework_language(Framework.DJANGO, Language.TYPESCRIPT)
        assert result is not None
        assert result.suggestions is not None
        assert len(result.suggestions) > 0
        assert all(isinstance(s, str) for s in result.suggestions)


class TestValidatePackageManagerLanguage:
    """Tests for validate_package_manager_language function."""

    def test_valid_python_package_managers(self):
        """Test all valid Python package managers return None."""
        valid_pms = [
            PackageManager.UV,
            PackageManager.POETRY,
            PackageManager.PIP,
            PackageManager.PIPENV,
        ]
        for pm in valid_pms:
            result = validate_package_manager_language(pm, Language.PYTHON)
            assert result is None, f"{pm.value} should be valid for Python"

    def test_valid_typescript_package_managers(self):
        """Test all valid TypeScript package managers return None."""
        valid_pms = [
            PackageManager.NPM,
            PackageManager.YARN,
            PackageManager.PNPM,
            PackageManager.BUN,
        ]
        for pm in valid_pms:
            result = validate_package_manager_language(pm, Language.TYPESCRIPT)
            assert result is None, f"{pm.value} should be valid for TypeScript"

    def test_valid_javascript_package_managers(self):
        """Test all valid JavaScript package managers return None."""
        valid_pms = [
            PackageManager.NPM,
            PackageManager.YARN,
            PackageManager.PNPM,
            PackageManager.BUN,
        ]
        for pm in valid_pms:
            result = validate_package_manager_language(pm, Language.JAVASCRIPT)
            assert result is None, f"{pm.value} should be valid for JavaScript"

    def test_valid_go_package_manager(self):
        """Test Go has only go modules as package manager."""
        result = validate_package_manager_language(PackageManager.GO_MOD, Language.GO)
        assert result is None

    def test_valid_rust_package_manager(self):
        """Test Rust has only cargo as package manager."""
        result = validate_package_manager_language(PackageManager.CARGO, Language.RUST)
        assert result is None

    def test_valid_java_package_managers(self):
        """Test all valid Java package managers return None."""
        valid_pms = [PackageManager.MAVEN, PackageManager.GRADLE]
        for pm in valid_pms:
            result = validate_package_manager_language(pm, Language.JAVA)
            assert result is None, f"{pm.value} should be valid for Java"

    def test_invalid_npm_with_python(self):
        """Test npm is invalid for Python."""
        result = validate_package_manager_language(PackageManager.NPM, Language.PYTHON)
        assert result is not None
        assert isinstance(result, ValidationIssue)
        assert result.field_name == "package_manager"
        assert result.invalid_value == "npm"
        assert "not compatible" in result.message.lower()
        assert result.suggestions is not None
        assert "uv" in result.suggestions
        assert "poetry" in result.suggestions

    def test_invalid_uv_with_go(self):
        """Test uv is invalid for Go."""
        result = validate_package_manager_language(PackageManager.UV, Language.GO)
        assert result is not None
        assert isinstance(result, ValidationIssue)
        assert result.field_name == "package_manager"
        assert result.invalid_value == "uv"
        assert result.suggestions is not None
        assert "go" in result.suggestions

    def test_invalid_cargo_with_python(self):
        """Test cargo is invalid for Python."""
        result = validate_package_manager_language(PackageManager.CARGO, Language.PYTHON)
        assert result is not None
        assert isinstance(result, ValidationIssue)
        assert result.field_name == "package_manager"
        assert result.invalid_value == "cargo"
        assert result.suggestions is not None

    def test_invalid_maven_with_typescript(self):
        """Test Maven is invalid for TypeScript."""
        result = validate_package_manager_language(PackageManager.MAVEN, Language.TYPESCRIPT)
        assert result is not None
        assert isinstance(result, ValidationIssue)
        assert result.field_name == "package_manager"
        assert result.invalid_value == "maven"
        assert result.suggestions is not None
        assert "npm" in result.suggestions

    def test_suggestions_are_populated(self):
        """Test that invalid combinations include suggestions."""
        result = validate_package_manager_language(PackageManager.YARN, Language.PYTHON)
        assert result is not None
        assert result.suggestions is not None
        assert len(result.suggestions) > 0
        assert all(isinstance(s, str) for s in result.suggestions)


class TestValidateArchitectureFramework:
    """Tests for validate_architecture_framework function."""

    def test_simple_architecture_with_any_framework(self):
        """Test Simple architecture is valid with any framework."""
        all_frameworks = [
            Framework.FASTAPI,
            Framework.DJANGO,
            Framework.FLASK,
            Framework.NEXTJS,
            Framework.EXPRESS,
            Framework.NESTJS,
            Framework.GIN,
            Framework.ECHO,
            Framework.AXUM,
            Framework.ACTIX,
            Framework.SPRING,
            Framework.NONE,
        ]
        for framework in all_frameworks:
            result = validate_architecture_framework(Architecture.SIMPLE, framework)
            assert (
                result is None
            ), f"Simple architecture should work with {framework.value}"

    def test_layered_architecture_with_any_framework(self):
        """Test Layered architecture is valid with any framework."""
        all_frameworks = [
            Framework.FASTAPI,
            Framework.DJANGO,
            Framework.NEXTJS,
            Framework.GIN,
            Framework.AXUM,
            Framework.SPRING,
            Framework.NONE,
        ]
        for framework in all_frameworks:
            result = validate_architecture_framework(Architecture.LAYERED, framework)
            assert (
                result is None
            ), f"Layered architecture should work with {framework.value}"

    def test_ddd_with_substantial_framework(self):
        """Test DDD architecture is valid with substantial frameworks."""
        substantial_frameworks = [
            Framework.FASTAPI,
            Framework.DJANGO,
            Framework.NESTJS,
            Framework.SPRING,
        ]
        for framework in substantial_frameworks:
            result = validate_architecture_framework(Architecture.DDD, framework)
            assert (
                result is None
            ), f"DDD architecture should work with {framework.value}"

    def test_clean_with_substantial_framework(self):
        """Test Clean architecture is valid with substantial frameworks."""
        substantial_frameworks = [
            Framework.FASTAPI,
            Framework.FLASK,
            Framework.EXPRESS,
            Framework.GIN,
        ]
        for framework in substantial_frameworks:
            result = validate_architecture_framework(Architecture.CLEAN, framework)
            assert (
                result is None
            ), f"Clean architecture should work with {framework.value}"

    def test_hexagonal_with_substantial_framework(self):
        """Test Hexagonal architecture is valid with substantial frameworks."""
        substantial_frameworks = [
            Framework.FASTAPI,
            Framework.NESTJS,
            Framework.SPRING,
        ]
        for framework in substantial_frameworks:
            result = validate_architecture_framework(Architecture.HEXAGONAL, framework)
            assert (
                result is None
            ), f"Hexagonal architecture should work with {framework.value}"

    def test_ddd_with_none_framework_invalid(self):
        """Test DDD architecture is invalid with Framework.NONE."""
        result = validate_architecture_framework(Architecture.DDD, Framework.NONE)
        assert result is not None
        assert isinstance(result, ValidationIssue)
        assert result.field_name == "architecture"
        assert result.invalid_value == "ddd"
        assert "requires a substantial framework" in result.message.lower()
        assert result.suggestions is not None
        assert len(result.suggestions) > 0

    def test_clean_with_none_framework_invalid(self):
        """Test Clean architecture is invalid with Framework.NONE."""
        result = validate_architecture_framework(Architecture.CLEAN, Framework.NONE)
        assert result is not None
        assert isinstance(result, ValidationIssue)
        assert result.field_name == "architecture"
        assert result.invalid_value == "clean"
        assert "requires a substantial framework" in result.message.lower()
        assert result.suggestions is not None

    def test_hexagonal_with_none_framework_invalid(self):
        """Test Hexagonal architecture is invalid with Framework.NONE."""
        result = validate_architecture_framework(Architecture.HEXAGONAL, Framework.NONE)
        assert result is not None
        assert isinstance(result, ValidationIssue)
        assert result.field_name == "architecture"
        assert result.invalid_value == "hexagonal"
        assert "requires a substantial framework" in result.message.lower()
        assert result.suggestions is not None

    def test_suggestions_include_alternatives(self):
        """Test that suggestions include actionable alternatives."""
        result = validate_architecture_framework(Architecture.DDD, Framework.NONE)
        assert result is not None
        assert result.suggestions is not None
        assert any("SIMPLE" in s or "LAYERED" in s for s in result.suggestions)


class TestValidationIssueStructure:
    """Tests for ValidationIssue model structure."""

    def test_validation_issue_has_all_fields(self):
        """Test ValidationIssue has all required fields."""
        issue = ValidationIssue(
            message="Test message",
            field_name="test_field",
            invalid_value="test_value",
            suggestions=["suggestion1", "suggestion2"],
        )
        assert issue.message == "Test message"
        assert issue.field_name == "test_field"
        assert issue.invalid_value == "test_value"
        assert issue.suggestions == ["suggestion1", "suggestion2"]

    def test_validation_issue_suggestions_optional(self):
        """Test ValidationIssue suggestions can be None."""
        issue = ValidationIssue(
            message="Test message",
            field_name="test_field",
            invalid_value="test_value",
            suggestions=None,
        )
        assert issue.suggestions is None

    def test_validation_issue_from_real_validation(self):
        """Test ValidationIssue structure from real validation."""
        result = validate_framework_language(Framework.FASTAPI, Language.GO)
        assert result is not None
        assert hasattr(result, "message")
        assert hasattr(result, "field_name")
        assert hasattr(result, "invalid_value")
        assert hasattr(result, "suggestions")
        assert isinstance(result.message, str)
        assert isinstance(result.field_name, str)
        assert result.suggestions is None or isinstance(result.suggestions, list)


class TestCompatibilityMappings:
    """Tests for compatibility mapping constants."""

    def test_compatible_frameworks_covers_all_languages(self):
        """Test COMPATIBLE_FRAMEWORKS includes all languages."""
        expected_languages = {
            Language.PYTHON,
            Language.TYPESCRIPT,
            Language.JAVASCRIPT,
            Language.GO,
            Language.RUST,
            Language.JAVA,
        }
        actual_languages = set(COMPATIBLE_FRAMEWORKS.keys())
        assert actual_languages == expected_languages

    def test_compatible_package_managers_covers_all_languages(self):
        """Test COMPATIBLE_PACKAGE_MANAGERS includes all languages."""
        expected_languages = {
            Language.PYTHON,
            Language.TYPESCRIPT,
            Language.JAVASCRIPT,
            Language.GO,
            Language.RUST,
            Language.JAVA,
        }
        actual_languages = set(COMPATIBLE_PACKAGE_MANAGERS.keys())
        assert actual_languages == expected_languages

    def test_architectures_requiring_base_classes_correct(self):
        """Test ARCHITECTURES_REQUIRING_BASE_CLASSES contains expected values."""
        expected = {Architecture.DDD, Architecture.CLEAN, Architecture.HEXAGONAL}
        actual = set(ARCHITECTURES_REQUIRING_BASE_CLASSES)
        assert actual == expected

    def test_all_frameworks_mapped(self):
        """Test all Framework enum values are in compatibility mappings."""
        all_mapped_frameworks = set()
        for frameworks in COMPATIBLE_FRAMEWORKS.values():
            all_mapped_frameworks.update(frameworks)

        # All frameworks should be mapped to at least one language
        all_framework_values = set(Framework)
        assert all_framework_values == all_mapped_frameworks

    def test_all_package_managers_mapped(self):
        """Test all PackageManager enum values are in compatibility mappings."""
        all_mapped_pms = set()
        for pms in COMPATIBLE_PACKAGE_MANAGERS.values():
            all_mapped_pms.update(pms)

        # All package managers should be mapped to at least one language
        all_pm_values = set(PackageManager)
        assert all_pm_values == all_mapped_pms


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_framework_none_with_all_architectures(self):
        """Test Framework.NONE behavior with different architectures."""
        # Should be valid for Simple and Layered
        assert validate_architecture_framework(Architecture.SIMPLE, Framework.NONE) is None
        assert validate_architecture_framework(Architecture.LAYERED, Framework.NONE) is None

        # Should be invalid for DDD, Clean, Hexagonal
        assert (
            validate_architecture_framework(Architecture.DDD, Framework.NONE) is not None
        )
        assert (
            validate_architecture_framework(Architecture.CLEAN, Framework.NONE)
            is not None
        )
        assert (
            validate_architecture_framework(Architecture.HEXAGONAL, Framework.NONE)
            is not None
        )

    def test_typescript_javascript_share_package_managers(self):
        """Test TypeScript and JavaScript support same package managers."""
        ts_pms = set(COMPATIBLE_PACKAGE_MANAGERS[Language.TYPESCRIPT])
        js_pms = set(COMPATIBLE_PACKAGE_MANAGERS[Language.JAVASCRIPT])
        assert ts_pms == js_pms

    def test_go_rust_single_package_manager(self):
        """Test Go and Rust have single package manager option."""
        go_pms = COMPATIBLE_PACKAGE_MANAGERS[Language.GO]
        rust_pms = COMPATIBLE_PACKAGE_MANAGERS[Language.RUST]

        assert len(go_pms) == 1
        assert go_pms[0] == PackageManager.GO_MOD

        assert len(rust_pms) == 1
        assert rust_pms[0] == PackageManager.CARGO

    def test_all_languages_support_framework_none(self):
        """Test all languages support Framework.NONE."""
        all_languages = [
            Language.PYTHON,
            Language.TYPESCRIPT,
            Language.JAVASCRIPT,
            Language.GO,
            Language.RUST,
            Language.JAVA,
        ]
        for language in all_languages:
            frameworks = COMPATIBLE_FRAMEWORKS[language]
            assert (
                Framework.NONE in frameworks
            ), f"{language.value} should support Framework.NONE"
