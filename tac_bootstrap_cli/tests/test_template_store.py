"""Tests for the Package Template Store (Feature 6).

Comprehensive test suite covering template store infrastructure,
template store service, search, install, rating, and edge cases.
"""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest

from tac_bootstrap.infrastructure.template_store import TemplateMetadata, TemplateStore
from tac_bootstrap.application.template_store_service import TemplateStoreService


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def store_dir(tmp_path: Path) -> Path:
    """Create a temporary store directory."""
    return tmp_path / "template-store"


@pytest.fixture
def store(store_dir: Path) -> TemplateStore:
    """Create a TemplateStore with temporary directory."""
    return TemplateStore(store_dir=store_dir)


@pytest.fixture
def service(store: TemplateStore) -> TemplateStoreService:
    """Create a TemplateStoreService with test store."""
    return TemplateStoreService(store=store)


@pytest.fixture
def sample_template() -> TemplateMetadata:
    """Create a sample template."""
    return TemplateMetadata(
        id="test/my-template",
        name="My Template",
        description="A test template for unit testing",
        version="1.1.0",
        author="Test Author",
        tags=["python", "fastapi", "test"],
    )


@pytest.fixture
def populated_store(store: TemplateStore) -> TemplateStore:
    """Create a store with several templates."""
    templates = [
        TemplateMetadata(
            id="auth/jwt-template",
            name="JWT Auth Template",
            description="JWT authentication boilerplate",
            version="2.0.0",
            author="Auth Team",
            downloads=150,
            rating=4.5,
            rating_count=20,
            tags=["python", "auth", "jwt", "security"],
        ),
        TemplateMetadata(
            id="api/rest-starter",
            name="REST API Starter",
            description="REST API starter template with FastAPI",
            version="1.5.0",
            author="API Team",
            downloads=300,
            rating=4.8,
            rating_count=50,
            tags=["python", "fastapi", "rest", "api"],
        ),
        TemplateMetadata(
            id="frontend/react-app",
            name="React App",
            description="React application with TypeScript",
            version="3.0.0",
            author="Frontend Team",
            downloads=500,
            rating=4.2,
            rating_count=100,
            tags=["typescript", "react", "frontend"],
        ),
    ]
    for t in templates:
        store.add_template(t)
    return store


# ============================================================================
# TEST TEMPLATE METADATA
# ============================================================================


class TestTemplateMetadata:
    """Tests for TemplateMetadata Pydantic model."""

    def test_valid_template(self):
        """Valid template data should create metadata."""
        t = TemplateMetadata(id="user/template", name="Template", version="1.1.0")
        assert t.id == "user/template"
        assert t.downloads == 0
        assert t.rating == 0.0

    def test_empty_id_raises(self):
        """Empty ID should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            TemplateMetadata(id="", name="Template")

    def test_defaults(self):
        """Default values should be applied."""
        t = TemplateMetadata(id="test", name="Test")
        assert t.version == "1.1.0"
        assert t.author == ""
        assert t.tags == []
        assert t.installed is False
        assert t.install_path is None

    def test_rating_bounds(self):
        """Rating should be bounded 0-5."""
        t = TemplateMetadata(id="test", name="Test", rating=5.0)
        assert t.rating == 5.0

        with pytest.raises(ValueError):
            TemplateMetadata(id="test", name="Test", rating=6.0)

        with pytest.raises(ValueError):
            TemplateMetadata(id="test", name="Test", rating=-1.0)


# ============================================================================
# TEST TEMPLATE STORE
# ============================================================================


class TestTemplateStore:
    """Tests for TemplateStore infrastructure."""

    def test_store_initialization(self, store: TemplateStore):
        """Store should initialize with empty registry."""
        assert store.template_count == 0

    def test_add_template(self, store: TemplateStore, sample_template: TemplateMetadata):
        """Adding a template should increase count."""
        store.add_template(sample_template)
        assert store.template_count == 1

    def test_add_template_persistence(self, store_dir: Path, sample_template: TemplateMetadata):
        """Templates should persist across store instances."""
        store1 = TemplateStore(store_dir=store_dir)
        store1.add_template(sample_template)

        store2 = TemplateStore(store_dir=store_dir)
        assert store2.template_count == 1

    def test_remove_template(self, store: TemplateStore, sample_template: TemplateMetadata):
        """Removing a template should decrease count."""
        store.add_template(sample_template)
        assert store.remove_template("test/my-template") is True
        assert store.template_count == 0

    def test_remove_nonexistent(self, store: TemplateStore):
        """Removing nonexistent template should return False."""
        assert store.remove_template("nonexistent") is False

    def test_template_exists(self, store: TemplateStore, sample_template: TemplateMetadata):
        """template_exists should correctly check existence."""
        store.add_template(sample_template)
        assert store.template_exists("test/my-template") is True
        assert store.template_exists("nonexistent") is False

    def test_get_metadata(self, store: TemplateStore, sample_template: TemplateMetadata):
        """get_metadata should return dict representation."""
        store.add_template(sample_template)
        metadata = store.get_metadata("test/my-template")
        assert metadata is not None
        assert metadata["id"] == "test/my-template"
        assert metadata["name"] == "My Template"

    def test_get_metadata_nonexistent(self, store: TemplateStore):
        """get_metadata for nonexistent should return None."""
        assert store.get_metadata("nonexistent") is None

    def test_search_by_query(self, populated_store: TemplateStore):
        """Search should match against name, description, tags."""
        results = populated_store.search("fastapi")
        assert len(results) >= 1
        assert any("rest" in r.id for r in results)

    def test_search_by_tags_filter(self, populated_store: TemplateStore):
        """Search with tags filter should match."""
        results = populated_store.search(filters={"tags": ["security"]})
        assert len(results) >= 1
        assert results[0].id == "auth/jwt-template"

    def test_search_by_author_filter(self, populated_store: TemplateStore):
        """Search with author filter should match exactly."""
        results = populated_store.search(filters={"author": "Frontend Team"})
        assert len(results) == 1
        assert results[0].id == "frontend/react-app"

    def test_search_by_min_rating(self, populated_store: TemplateStore):
        """Search with min_rating filter should work."""
        results = populated_store.search(filters={"min_rating": 4.5})
        assert all(r.rating >= 4.5 for r in results)

    def test_search_empty_query(self, populated_store: TemplateStore):
        """Empty query should return all templates."""
        results = populated_store.search("")
        assert len(results) == 3

    def test_search_no_results(self, populated_store: TemplateStore):
        """Non-matching query should return empty list."""
        results = populated_store.search("nonexistent-query-12345")
        assert results == []

    def test_search_sorted_by_downloads(self, populated_store: TemplateStore):
        """Results should be sorted by downloads (most first)."""
        results = populated_store.search("")
        downloads = [r.downloads for r in results]
        assert downloads == sorted(downloads, reverse=True)

    def test_install(self, store: TemplateStore, sample_template: TemplateMetadata):
        """Install should mark template as installed."""
        store.add_template(sample_template)
        assert store.install("test/my-template") is True

        metadata = store.get_metadata("test/my-template")
        assert metadata["installed"] is True
        assert metadata["install_path"] is not None

    def test_install_nonexistent(self, store: TemplateStore):
        """Installing nonexistent template should return False."""
        assert store.install("nonexistent") is False

    def test_install_with_version(self, store: TemplateStore, sample_template: TemplateMetadata):
        """Install with explicit version should update version."""
        store.add_template(sample_template)
        store.install("test/my-template", version="2.0.0")

        metadata = store.get_metadata("test/my-template")
        assert metadata["version"] == "2.0.0"

    def test_uninstall(self, store: TemplateStore, sample_template: TemplateMetadata):
        """Uninstall should mark template as not installed."""
        store.add_template(sample_template)
        store.install("test/my-template")
        assert store.uninstall("test/my-template") is True

        metadata = store.get_metadata("test/my-template")
        assert metadata["installed"] is False

    def test_list_installed(self, store: TemplateStore, sample_template: TemplateMetadata):
        """list_installed should return only installed templates."""
        store.add_template(sample_template)
        assert len(store.list_installed()) == 0

        store.install("test/my-template")
        assert len(store.list_installed()) == 1

    def test_list_all(self, populated_store: TemplateStore):
        """list_all should return all templates sorted by name."""
        results = populated_store.list_all()
        assert len(results) == 3

    def test_rate_template(self, store: TemplateStore, sample_template: TemplateMetadata):
        """Rating should update average."""
        store.add_template(sample_template)
        store.rate("test/my-template", 5)
        metadata = store.get_metadata("test/my-template")
        assert metadata["rating"] == 5.0
        assert metadata["rating_count"] == 1

        store.rate("test/my-template", 3)
        metadata = store.get_metadata("test/my-template")
        assert metadata["rating"] == 4.0  # (5+3)/2
        assert metadata["rating_count"] == 2

    def test_rate_invalid_value(self, store: TemplateStore, sample_template: TemplateMetadata):
        """Invalid rating should raise ValueError."""
        store.add_template(sample_template)
        with pytest.raises(ValueError):
            store.rate("test/my-template", 6)
        with pytest.raises(ValueError):
            store.rate("test/my-template", 0)

    def test_rate_nonexistent(self, store: TemplateStore):
        """Rating nonexistent template should return False."""
        assert store.rate("nonexistent", 5) is False

    def test_seed_defaults(self, store: TemplateStore):
        """seed_defaults should add built-in templates."""
        store.seed_defaults()
        assert store.template_count >= 5

    def test_installed_count(self, store: TemplateStore, sample_template: TemplateMetadata):
        """installed_count property should track correctly."""
        store.add_template(sample_template)
        assert store.installed_count == 0
        store.install("test/my-template")
        assert store.installed_count == 1


# ============================================================================
# TEST TEMPLATE STORE SERVICE
# ============================================================================


class TestTemplateStoreService:
    """Tests for TemplateStoreService application layer."""

    def test_search_templates(self, service: TemplateStoreService, store: TemplateStore):
        """Service search should return dict results."""
        store.seed_defaults()
        results = service.search_templates("fastapi")
        assert isinstance(results, list)
        assert len(results) >= 1

    def test_install_template(self, service: TemplateStoreService, store: TemplateStore):
        """Service install should return success dict."""
        store.seed_defaults()
        result = service.install_template("tac/fastapi-starter")
        assert result["success"] is True

    def test_install_with_version_suffix(self, service: TemplateStoreService, store: TemplateStore):
        """Install with id:version format should parse correctly."""
        store.seed_defaults()
        result = service.install_template("tac/fastapi-starter:2.0.0")
        assert result["success"] is True

    def test_install_nonexistent(self, service: TemplateStoreService):
        """Install nonexistent should return failure."""
        result = service.install_template("nonexistent/template")
        assert result["success"] is False

    def test_uninstall_template(self, service: TemplateStoreService, store: TemplateStore):
        """Service uninstall should work."""
        store.seed_defaults()
        store.install("tac/fastapi-starter")
        result = service.uninstall_template("tac/fastapi-starter")
        assert result["success"] is True

    def test_list_installed_templates(self, service: TemplateStoreService, store: TemplateStore):
        """Service list_installed should return dicts."""
        store.seed_defaults()
        store.install("tac/fastapi-starter")
        installed = service.list_installed_templates()
        assert len(installed) == 1

    def test_rate_template(self, service: TemplateStoreService, store: TemplateStore):
        """Service rate should return success."""
        store.seed_defaults()
        result = service.rate_template("tac/fastapi-starter", 5)
        assert result["success"] is True
        assert "new_rating" in result

    def test_rate_invalid(self, service: TemplateStoreService, store: TemplateStore):
        """Invalid rating should return failure."""
        result = service.rate_template("whatever", 6)
        assert result["success"] is False

    def test_get_template_info(self, service: TemplateStoreService, store: TemplateStore):
        """get_template_info should return dict."""
        store.seed_defaults()
        info = service.get_template_info("tac/fastapi-starter")
        assert info is not None
        assert info["name"] == "FastAPI Starter"

    def test_add_template(self, service: TemplateStoreService):
        """Service add_template should work."""
        result = service.add_template(
            template_id="custom/template",
            name="Custom Template",
            description="A custom template",
            author="Custom Author",
            tags=["custom"],
        )
        assert result["success"] is True
        assert service.template_count == 1

    def test_seed_defaults(self, service: TemplateStoreService):
        """seed_defaults should return count."""
        count = service.seed_defaults()
        assert count >= 5

    def test_template_count(self, service: TemplateStoreService):
        """template_count should track."""
        assert service.template_count == 0
        service.seed_defaults()
        assert service.template_count >= 5
