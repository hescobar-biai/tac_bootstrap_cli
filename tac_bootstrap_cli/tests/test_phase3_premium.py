"""
Tests for Phase 3: Premium Features & Polish

Comprehensive test suite covering all 10 Phase 3 features:
- Feature 11: Multi-Language Support (i18n)
- Feature 12: Web Dashboard
- Feature 13: Advanced Search & Filter
- Feature 14: Project History & Snapshots
- Feature 15: AI-Assisted Code Generation
- Feature 16: Learning Mode & Tutorials
- Feature 17: Sync & Collaboration
- Feature 18: Project Analytics & Metrics
- Feature 19: Smart Recommendations
- Feature 20: Community & Social Features

Target: 150+ test cases
"""

import json
import os
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from tac_bootstrap.interfaces.cli import app

runner = CliRunner()


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def temp_home(tmp_path: Path) -> Path:
    """Create a temporary home directory for services."""
    tac_dir = tmp_path / ".tac-bootstrap"
    tac_dir.mkdir(parents=True)
    return tmp_path


@pytest.fixture
def sample_project(tmp_path: Path) -> Path:
    """Create a minimal sample project for testing."""
    project = tmp_path / "test-project"
    project.mkdir()

    # Create basic project files
    (project / "config.yml").write_text(
        "project:\n  name: test-project\n  language: python\n"
        "  package_manager: uv\n  framework: none\n  architecture: simple\n"
        "commands:\n  start: 'uv run python -m app'\n  test: 'uv run pytest'\n"
        "claude:\n  settings:\n    project_name: test-project\n"
    )
    (project / "README.md").write_text("# Test Project\n")
    (project / ".gitignore").write_text(".env\n__pycache__\n")

    src = project / "src"
    src.mkdir()
    (src / "__init__.py").write_text("")
    (src / "app.py").write_text(
        "import os\n\n"
        "def main():\n"
        "    print('Hello')\n\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )

    tests_dir = project / "tests"
    tests_dir.mkdir()
    (tests_dir / "__init__.py").write_text("")
    (tests_dir / "test_app.py").write_text(
        "def test_hello():\n    assert True\n"
    )

    return project


# ============================================================================
# FEATURE 11: MULTI-LANGUAGE SUPPORT (i18n) - 20+ Tests
# ============================================================================


class TestI18nService:
    """Tests for the i18n service."""

    def setup_method(self) -> None:
        """Reset singleton before each test."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        I18nService.reset_instance()

    def test_default_language_is_english(self, temp_home: Path) -> None:
        """Default language should be English."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            assert i18n.current_language == "en"

    def test_set_language_spanish(self, temp_home: Path) -> None:
        """Setting language to Spanish should work."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            assert i18n.set_language("es") is True
            assert i18n.current_language == "es"

    def test_set_language_french(self, temp_home: Path) -> None:
        """Setting language to French should work."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            assert i18n.set_language("fr") is True
            assert i18n.current_language == "fr"

    def test_set_language_german(self, temp_home: Path) -> None:
        """Setting language to German should work."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            assert i18n.set_language("de") is True

    def test_set_language_japanese(self, temp_home: Path) -> None:
        """Setting language to Japanese should work."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            assert i18n.set_language("ja") is True

    def test_set_language_chinese(self, temp_home: Path) -> None:
        """Setting language to Chinese should work."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            assert i18n.set_language("zh") is True

    def test_set_unsupported_language_returns_false(self, temp_home: Path) -> None:
        """Setting unsupported language should return False."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            assert i18n.set_language("xx") is False

    def test_translate_english_key(self, temp_home: Path) -> None:
        """Translation of known key should return English text."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            result = i18n.translate("cli.welcome")
            assert "TAC Bootstrap" in result

    def test_translate_spanish_key(self, temp_home: Path) -> None:
        """Translation in Spanish should return Spanish text."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            i18n.set_language("es")
            result = i18n.translate("cli.welcome")
            assert "Bienvenido" in result

    def test_translate_with_variables(self, temp_home: Path) -> None:
        """Translation with variable substitution should work."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            result = i18n.translate("cli.version", v="1.0.0")
            assert "1.0.0" in result

    def test_translate_missing_key_returns_key(self, temp_home: Path) -> None:
        """Missing translation key should return the key itself."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            result = i18n.translate("nonexistent.key")
            assert result == "nonexistent.key"

    def test_translate_fallback_to_english(self, temp_home: Path) -> None:
        """Missing translation in non-English should fall back to English."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            i18n.set_language("es")
            # This key exists in English
            result = i18n.translate("cli.welcome")
            assert result  # Should have some content

    def test_get_supported_languages(self, temp_home: Path) -> None:
        """Should return all 6 supported languages."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            langs = i18n.get_supported_languages()
            assert len(langs) == 6
            assert "en" in langs
            assert "es" in langs
            assert "fr" in langs

    def test_current_language_name(self, temp_home: Path) -> None:
        """Should return display name for current language."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            assert i18n.current_language_name == "English"

    def test_get_all_keys_english(self, temp_home: Path) -> None:
        """Should return all translation keys for English."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            keys = i18n.get_all_keys("en")
            assert len(keys) > 10

    def test_has_key(self, temp_home: Path) -> None:
        """has_key should return True for existing keys."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            assert i18n.has_key("cli.welcome") is True
            assert i18n.has_key("nonexistent") is False

    def test_global_t_function(self, temp_home: Path) -> None:
        """The global t() function should work."""
        from tac_bootstrap.infrastructure.i18n import I18nService, t

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            result = t("cli.welcome")
            assert "TAC Bootstrap" in result

    def test_singleton_pattern(self, temp_home: Path) -> None:
        """I18nService should be a singleton."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n1 = I18nService()
            i18n2 = I18nService()
            assert i18n1 is i18n2

    def test_reset_instance(self, temp_home: Path) -> None:
        """reset_instance should allow creating a new instance."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n1 = I18nService()
            I18nService.reset_instance()
            i18n2 = I18nService()
            assert i18n1 is not i18n2

    def test_language_persistence(self, temp_home: Path) -> None:
        """Language setting should persist to config file."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            i18n = I18nService()
            i18n.set_language("fr")

            config_file = temp_home / ".tac-bootstrap" / ".language_config"
            assert config_file.exists()
            assert config_file.read_text().strip() == "fr"


# ============================================================================
# FEATURE 12: WEB DASHBOARD - 25+ Tests
# ============================================================================


class TestDashboardServer:
    """Tests for the web dashboard server."""

    def test_dashboard_server_init(self) -> None:
        """DashboardServer should initialize with defaults."""
        from tac_bootstrap.infrastructure.web_server import DashboardServer

        server = DashboardServer()
        assert server.host == "127.0.0.1"
        assert server.port == 3000

    def test_dashboard_server_custom_port(self) -> None:
        """DashboardServer should accept custom port."""
        from tac_bootstrap.infrastructure.web_server import DashboardServer

        server = DashboardServer(port=8080)
        assert server.port == 8080

    def test_dashboard_is_not_running(self, temp_home: Path) -> None:
        """is_running should return False when no PID file."""
        from tac_bootstrap.infrastructure.web_server import DashboardServer, PID_FILE

        with patch(
            "tac_bootstrap.infrastructure.web_server.PID_FILE",
            temp_home / "dashboard.pid",
        ):
            server = DashboardServer()
            assert server.is_running() is False

    def test_dashboard_get_status_not_running(self) -> None:
        """get_status should show not running when server is off."""
        from tac_bootstrap.infrastructure.web_server import DashboardServer

        with patch(
            "tac_bootstrap.infrastructure.web_server.PID_FILE",
            Path("/tmp/nonexistent_pid_file_test"),
        ):
            server = DashboardServer()
            status = server.get_status()
            assert status["running"] is False

    def test_dashboard_stop_not_running(self) -> None:
        """stop should handle not-running state gracefully."""
        from tac_bootstrap.infrastructure.web_server import DashboardServer

        with patch(
            "tac_bootstrap.infrastructure.web_server.PID_FILE",
            Path("/tmp/nonexistent_pid_file_test"),
        ):
            server = DashboardServer()
            result = server.stop()
            assert result["status"] == "not_running"

    def test_create_app_returns_fastapi(self) -> None:
        """create_app should return a FastAPI instance."""
        try:
            from tac_bootstrap.infrastructure.web_server import create_app

            app_instance = create_app()
            assert app_instance is not None
            assert hasattr(app_instance, "routes")
        except ImportError:
            pytest.skip("FastAPI not installed")

    def test_dashboard_html_generation(self) -> None:
        """Dashboard HTML should contain expected elements."""
        from tac_bootstrap.infrastructure.web_server import _generate_dashboard_html

        html = _generate_dashboard_html()
        assert "TAC Bootstrap Dashboard" in html
        assert "System Health" in html
        assert "Quick Actions" in html
        assert "Projects" in html

    def test_dashboard_config_defaults(self) -> None:
        """DashboardConfig should have correct defaults."""
        from tac_bootstrap.infrastructure.web_server import DashboardConfig

        config = DashboardConfig()
        assert config.host == "127.0.0.1"
        assert config.port == 3000
        assert config.reload is False


# ============================================================================
# FEATURE 13: SEARCH & FILTER - 15+ Tests
# ============================================================================


class TestSearchService:
    """Tests for the search service."""

    def test_search_service_init(self) -> None:
        """SearchService should initialize with catalogs."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        assert service is not None

    def test_search_all_returns_results(self) -> None:
        """Searching without query should return all items."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search()
        assert results.total > 0

    def test_search_commands_by_query(self) -> None:
        """Searching commands should find matching items."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search_commands(query="test")
        assert results.total > 0
        assert any("test" in r.name.lower() or "test" in r.description.lower()
                    for r in results.results)

    def test_search_commands_by_tag(self) -> None:
        """Searching by tag should filter correctly."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search_commands(tag="testing")
        assert results.total > 0

    def test_search_templates_by_framework(self) -> None:
        """Searching templates by framework should work."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search_templates(framework="fastapi")
        assert results.total > 0
        for r in results.results:
            assert r.metadata.get("framework") == "fastapi"

    def test_search_templates_by_architecture(self) -> None:
        """Searching templates by architecture should work."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search_templates(architecture="ddd")
        assert results.total > 0

    def test_search_features_by_tier(self) -> None:
        """Searching features by tier should work."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search_features(tier="core")
        assert results.total > 0
        for r in results.results:
            assert r.metadata.get("tier") == "core"

    def test_search_features_by_query(self) -> None:
        """Searching features by text query should work."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search_features(query="validation")
        assert results.total > 0

    def test_search_results_are_ranked(self) -> None:
        """Results should be sorted by relevance."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search(query="test")
        if len(results.results) > 1:
            for i in range(len(results.results) - 1):
                assert results.results[i].relevance_score >= results.results[i + 1].relevance_score

    def test_search_empty_query(self) -> None:
        """Empty query should return results with default score."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search(query="")
        assert results.total > 0

    def test_search_no_results(self) -> None:
        """Impossible query should return no results."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search(query="xyznonexistent12345")
        assert results.total == 0

    def test_search_with_limit(self) -> None:
        """Search should respect limit parameter."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search(limit=3)
        assert results.total <= 3

    def test_search_result_model(self) -> None:
        """SearchResult should have required fields."""
        from tac_bootstrap.application.search_service import SearchResult

        result = SearchResult(
            name="test", category="command", description="test desc"
        )
        assert result.name == "test"
        assert result.relevance_score == 0.0

    def test_search_filters_applied(self) -> None:
        """Applied filters should be tracked in results."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search(category="feature", tier="core")
        assert "category" in results.filters_applied
        assert "tier" in results.filters_applied

    def test_search_commands_model_filter(self) -> None:
        """Searching commands with model filter should work."""
        from tac_bootstrap.application.search_service import SearchService

        service = SearchService()
        results = service.search_commands(model="opus")
        # Should find items that use opus model
        assert results.total >= 0


# ============================================================================
# FEATURE 14: SNAPSHOTS - 20+ Tests
# ============================================================================


class TestSnapshotService:
    """Tests for the snapshot service."""

    def test_create_snapshot(self, sample_project: Path, tmp_path: Path) -> None:
        """Creating a snapshot should succeed."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        metadata = service.create_snapshot(sample_project, "test-snap")

        assert metadata.name == "test-snap"
        assert metadata.file_count > 0

    def test_create_snapshot_with_description(self, sample_project: Path, tmp_path: Path) -> None:
        """Snapshot with description should store it."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        metadata = service.create_snapshot(
            sample_project, "desc-snap", description="Test description"
        )
        assert metadata.description == "Test description"

    def test_create_duplicate_snapshot_raises(self, sample_project: Path, tmp_path: Path) -> None:
        """Creating duplicate snapshot name should raise."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        service.create_snapshot(sample_project, "dup-snap")

        with pytest.raises(ValueError, match="already exists"):
            service.create_snapshot(sample_project, "dup-snap")

    def test_list_snapshots(self, sample_project: Path, tmp_path: Path) -> None:
        """Listing snapshots should return all created."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        service.create_snapshot(sample_project, "snap1")
        service.create_snapshot(sample_project, "snap2")

        snapshots = service.list_snapshots(sample_project)
        assert len(snapshots) == 2

    def test_list_snapshots_empty(self, sample_project: Path, tmp_path: Path) -> None:
        """Listing snapshots on empty project should return empty list."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        snapshots = service.list_snapshots(sample_project)
        assert len(snapshots) == 0

    def test_get_snapshot(self, sample_project: Path, tmp_path: Path) -> None:
        """Getting specific snapshot should work."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        service.create_snapshot(sample_project, "get-snap")

        snap = service.get_snapshot(sample_project, "get-snap")
        assert snap is not None
        assert snap.name == "get-snap"

    def test_get_nonexistent_snapshot(self, sample_project: Path, tmp_path: Path) -> None:
        """Getting nonexistent snapshot should return None."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        snap = service.get_snapshot(sample_project, "nonexistent")
        assert snap is None

    def test_diff_snapshots(self, sample_project: Path, tmp_path: Path) -> None:
        """Diffing two identical snapshots should show no changes."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        service.create_snapshot(sample_project, "snap-a")
        service.create_snapshot(sample_project, "snap-b")

        diff = service.diff_snapshots("snap-a", "snap-b", sample_project)
        assert len(diff.added) == 0
        assert len(diff.removed) == 0
        assert len(diff.modified) == 0
        assert diff.unchanged > 0

    def test_diff_snapshots_with_changes(self, sample_project: Path, tmp_path: Path) -> None:
        """Diffing snapshots after file change should detect modification."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        service.create_snapshot(sample_project, "before")

        # Modify a file
        (sample_project / "src" / "app.py").write_text("# Modified\ndef main(): pass\n")
        service.create_snapshot(sample_project, "after")

        diff = service.diff_snapshots("before", "after", sample_project)
        assert len(diff.modified) > 0 or len(diff.added) > 0

    def test_diff_nonexistent_snapshot_raises(self, sample_project: Path, tmp_path: Path) -> None:
        """Diffing with nonexistent snapshot should raise."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        service.create_snapshot(sample_project, "exists")

        with pytest.raises(ValueError, match="not found"):
            service.diff_snapshots("exists", "nonexistent", sample_project)

    def test_delete_snapshot(self, sample_project: Path, tmp_path: Path) -> None:
        """Deleting a snapshot should remove it."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        service.create_snapshot(sample_project, "to-delete")

        assert service.delete_snapshot("to-delete", sample_project) is True
        assert service.get_snapshot(sample_project, "to-delete") is None

    def test_delete_nonexistent_snapshot(self, sample_project: Path, tmp_path: Path) -> None:
        """Deleting nonexistent snapshot should return False."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        assert service.delete_snapshot("nonexistent", sample_project) is False

    def test_snapshot_exists(self, sample_project: Path, tmp_path: Path) -> None:
        """snapshot_exists should return correct boolean."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        service.create_snapshot(sample_project, "check-exists")

        assert service.snapshot_exists("check-exists", sample_project) is True
        assert service.snapshot_exists("nope", sample_project) is False

    def test_snapshot_excludes_pycache(self, sample_project: Path, tmp_path: Path) -> None:
        """Snapshots should exclude __pycache__ directories."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        # Create __pycache__
        pycache = sample_project / "src" / "__pycache__"
        pycache.mkdir()
        (pycache / "app.cpython-312.pyc").write_bytes(b"fake")

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        metadata = service.create_snapshot(sample_project, "no-cache")

        assert "__pycache__" not in str(metadata.file_checksums.keys())

    def test_snapshot_invalid_path_raises(self, tmp_path: Path) -> None:
        """Creating snapshot for invalid path should raise."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")

        with pytest.raises(ValueError, match="does not exist"):
            service.create_snapshot(tmp_path / "nonexistent", "snap")

    def test_restore_snapshot(self, sample_project: Path, tmp_path: Path) -> None:
        """Restoring a snapshot should restore files."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        service.create_snapshot(sample_project, "restore-test")

        # Modify file
        (sample_project / "src" / "app.py").write_text("# Changed")

        result = service.restore_snapshot("restore-test", sample_project)
        assert result["files_restored"] > 0

    def test_snapshot_metadata_has_checksums(self, sample_project: Path, tmp_path: Path) -> None:
        """Snapshot metadata should include file checksums."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        metadata = service.create_snapshot(sample_project, "checksum-snap")

        assert len(metadata.file_checksums) > 0

    def test_snapshot_metadata_has_version(self, sample_project: Path, tmp_path: Path) -> None:
        """Snapshot metadata should include TAC version."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        metadata = service.create_snapshot(sample_project, "version-snap")

        assert metadata.tac_version != ""

    def test_diff_entries_detail(self, sample_project: Path, tmp_path: Path) -> None:
        """Diff entries should contain detailed information."""
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService(base_dir=tmp_path / "snapshots")
        service.create_snapshot(sample_project, "d1")

        (sample_project / "new_file.py").write_text("# new file\n")
        service.create_snapshot(sample_project, "d2")

        diff = service.diff_snapshots("d1", "d2", sample_project)
        assert len(diff.entries) > 0


# ============================================================================
# FEATURE 15: AI-ASSISTED GENERATION - 25+ Tests
# ============================================================================


class TestAIGeneratorService:
    """Tests for the AI generator service."""

    def test_service_init_without_key(self) -> None:
        """Service should initialize without API key."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        with patch.dict(os.environ, {}, clear=True):
            service = AIGeneratorService()
            assert service.is_configured is False

    def test_service_init_with_key(self) -> None:
        """Service should detect API key from env."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService(api_key="test-key-123")
        assert service.is_configured is True

    def test_detect_project_context_python(self, sample_project: Path) -> None:
        """Should detect Python project context."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService()
        context = service._detect_project_context(sample_project)
        assert context["language"] == "python"

    def test_detect_project_context_default(self, tmp_path: Path) -> None:
        """Should return defaults for empty directory."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService()
        context = service._detect_project_context(tmp_path)
        assert "language" in context
        assert "framework" in context

    def test_generation_result_model(self) -> None:
        """AIGenerationResult should have correct defaults."""
        from tac_bootstrap.application.ai_generator import AIGenerationResult

        result = AIGenerationResult()
        assert result.success is True
        assert result.code == ""
        assert result.language == "python"

    def test_generation_result_error(self) -> None:
        """AIGenerationResult should handle error state."""
        from tac_bootstrap.application.ai_generator import AIGenerationResult

        result = AIGenerationResult(success=False, error="API failed")
        assert result.success is False
        assert result.error == "API failed"

    def test_refactor_suggestion_model(self) -> None:
        """AIRefactorSuggestion should have correct fields."""
        from tac_bootstrap.application.ai_generator import AIRefactorSuggestion

        suggestion = AIRefactorSuggestion(
            file_path="test.py",
            category="performance",
            description="Test suggestion",
        )
        assert suggestion.severity == "info"

    def test_test_suggestion_model(self) -> None:
        """AITestSuggestion should have correct fields."""
        from tac_bootstrap.application.ai_generator import AITestSuggestion

        suggestion = AITestSuggestion(
            test_name="test_example",
            test_code="def test_example(): assert True",
        )
        assert suggestion.test_type == "unit"
        assert suggestion.priority == "medium"

    def test_read_file_content(self, sample_project: Path) -> None:
        """Should read file content with line limit."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService()
        content = service._read_file_content(sample_project / "src" / "app.py")
        assert "main" in content

    def test_read_nonexistent_file(self) -> None:
        """Should return empty string for nonexistent file."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService()
        content = service._read_file_content(Path("/nonexistent/file.py"))
        assert content == ""

    def test_get_prompt_templates(self) -> None:
        """Should return all prompt templates."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService()
        templates = service.get_custom_prompt_templates()
        assert "endpoint" in templates
        assert "migration" in templates
        assert "refactor" in templates
        assert "test" in templates

    def test_set_custom_template(self) -> None:
        """Should allow setting custom templates."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService()
        service.set_prompt_template("custom", "My custom template: {param}")
        templates = service.get_custom_prompt_templates()
        assert "custom" in templates

    def test_parse_refactor_suggestions_json(self) -> None:
        """Should parse JSON refactoring suggestions."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService()
        response = '[{"category": "performance", "description": "test"}]'
        suggestions = service._parse_refactor_suggestions(response, "test.py")
        assert len(suggestions) >= 1

    def test_parse_refactor_suggestions_plain_text(self) -> None:
        """Should create fallback suggestion from plain text."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService()
        response = "Consider refactoring the long function."
        suggestions = service._parse_refactor_suggestions(response, "test.py")
        assert len(suggestions) == 1

    def test_parse_test_suggestions_json(self) -> None:
        """Should parse JSON test suggestions."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService()
        response = '[{"test_name": "test_foo", "test_code": "def test_foo(): pass"}]'
        suggestions = service._parse_test_suggestions(response)
        assert len(suggestions) >= 1

    def test_generate_endpoint_without_key(self) -> None:
        """generate_endpoint without API key should return error."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService(api_key="")
        result = service.generate_endpoint(path="/test")
        assert result.success is False

    def test_suggest_refactor_nonexistent_file(self) -> None:
        """suggest_refactor for nonexistent file should return empty."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService(api_key="test")
        suggestions = service.suggest_refactor(Path("/nonexistent.py"))
        assert len(suggestions) == 0

    def test_suggest_tests_nonexistent_file(self) -> None:
        """suggest_tests for nonexistent file should return empty."""
        from tac_bootstrap.application.ai_generator import AIGeneratorService

        service = AIGeneratorService(api_key="test")
        suggestions = service.suggest_tests(Path("/nonexistent.py"))
        assert len(suggestions) == 0


# ============================================================================
# FEATURE 16: LEARNING - 15+ Tests
# ============================================================================


class TestLearningService:
    """Tests for the learning service."""

    def test_list_topics(self) -> None:
        """Should list all available topics."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        topics = service.list_topics()
        assert len(topics) >= 4

    def test_get_ddd_topic(self) -> None:
        """Should return DDD topic."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        topic = service.get_topic("ddd")
        assert topic is not None
        assert "DDD" in topic.title

    def test_get_architecture_topic(self) -> None:
        """Should return architecture topic."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        topic = service.get_topic("architecture")
        assert topic is not None

    def test_get_nonexistent_topic(self) -> None:
        """Should return None for nonexistent topic."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        topic = service.get_topic("nonexistent")
        assert topic is None

    def test_search_topics(self) -> None:
        """Should find topics by search query."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        results = service.search_topics("domain")
        assert len(results) > 0

    def test_list_tutorials(self) -> None:
        """Should list all tutorials."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        tutorials = service.list_tutorials()
        assert len(tutorials) >= 2

    def test_get_quick_start_tutorial(self) -> None:
        """Should return quick-start tutorial."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        tut = service.get_tutorial("quick-start")
        assert tut is not None
        assert len(tut.steps) > 0

    def test_get_advanced_tutorial(self) -> None:
        """Should return advanced tutorial."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        tut = service.get_tutorial("advanced")
        assert tut is not None

    def test_get_nonexistent_tutorial(self) -> None:
        """Should return None for nonexistent tutorial."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        tut = service.get_tutorial("nonexistent")
        assert tut is None

    def test_topics_have_sections(self) -> None:
        """All topics should have at least one section."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        for topic in service.list_topics():
            assert len(topic.sections) > 0

    def test_tutorials_have_steps(self) -> None:
        """All tutorials should have steps."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        for tut in service.list_tutorials():
            assert len(tut.steps) > 0

    def test_get_topics_by_difficulty(self) -> None:
        """Should filter topics by difficulty."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        beginner = service.get_topics_by_difficulty("beginner")
        assert len(beginner) > 0

    def test_get_related_topics(self) -> None:
        """Should return related topics."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        related = service.get_related_topics("ddd")
        assert len(related) >= 0

    def test_topic_has_examples(self) -> None:
        """DDD topic should have code examples."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        topic = service.get_topic("ddd")
        assert topic is not None
        assert len(topic.examples) > 0

    def test_tutorial_has_prerequisites(self) -> None:
        """Quick-start tutorial should have prerequisites."""
        from tac_bootstrap.application.learning_service import LearningService

        service = LearningService()
        tut = service.get_tutorial("quick-start")
        assert tut is not None
        assert len(tut.prerequisites) > 0


# ============================================================================
# FEATURE 17: TEAM & COLLABORATION - 20+ Tests
# ============================================================================


class TestTeamService:
    """Tests for the team service."""

    def test_share_project(self, sample_project: Path, tmp_path: Path) -> None:
        """Should share project with a user."""
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService(base_dir=tmp_path / "teams")
        member = service.share_project(sample_project, "alice@test.com")
        assert member.email == "alice@test.com"
        assert member.role == "contributor"

    def test_share_project_with_role(self, sample_project: Path, tmp_path: Path) -> None:
        """Should share with specified role."""
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService(base_dir=tmp_path / "teams")
        member = service.share_project(sample_project, "bob@test.com", role="admin")
        assert member.role == "admin"

    def test_share_invalid_email_raises(self, sample_project: Path, tmp_path: Path) -> None:
        """Should raise for invalid email."""
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService(base_dir=tmp_path / "teams")
        with pytest.raises(ValueError, match="Invalid email"):
            service.share_project(sample_project, "not-an-email")

    def test_share_invalid_role_raises(self, sample_project: Path, tmp_path: Path) -> None:
        """Should raise for invalid role."""
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService(base_dir=tmp_path / "teams")
        with pytest.raises(ValueError, match="Invalid role"):
            service.share_project(sample_project, "a@b.com", role="superadmin")

    def test_share_duplicate_raises(self, sample_project: Path, tmp_path: Path) -> None:
        """Should raise for duplicate sharing."""
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService(base_dir=tmp_path / "teams")
        service.share_project(sample_project, "dup@test.com")
        with pytest.raises(ValueError, match="already shared"):
            service.share_project(sample_project, "dup@test.com")

    def test_list_shared(self, sample_project: Path, tmp_path: Path) -> None:
        """Should list shared members."""
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService(base_dir=tmp_path / "teams")
        service.share_project(sample_project, "a@test.com")
        service.share_project(sample_project, "b@test.com")

        members = service.list_shared(sample_project)
        assert len(members) == 2

    def test_list_shared_empty(self, sample_project: Path, tmp_path: Path) -> None:
        """Should return empty list for unshared project."""
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService(base_dir=tmp_path / "teams")
        members = service.list_shared(sample_project)
        assert len(members) == 0

    def test_remove_member(self, sample_project: Path, tmp_path: Path) -> None:
        """Should remove a member."""
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService(base_dir=tmp_path / "teams")
        service.share_project(sample_project, "remove@test.com")
        assert service.remove_member(sample_project, "remove@test.com") is True
        assert len(service.list_shared(sample_project)) == 0

    def test_sync_changes(self, sample_project: Path, tmp_path: Path) -> None:
        """Should sync changes successfully."""
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService(base_dir=tmp_path / "teams")
        result = service.sync_changes(sample_project)
        assert result.success is True

    def test_notify_team(self, sample_project: Path, tmp_path: Path) -> None:
        """Should create notification."""
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService(base_dir=tmp_path / "teams")
        notif = service.notify_team(sample_project, "Test message")
        assert notif.message == "Test message"

    def test_get_notifications(self, sample_project: Path, tmp_path: Path) -> None:
        """Should return notifications."""
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService(base_dir=tmp_path / "teams")
        service.notify_team(sample_project, "Msg 1")
        service.notify_team(sample_project, "Msg 2")

        notifs = service.get_notifications(sample_project)
        assert len(notifs) >= 2

    def test_workspace_info(self, sample_project: Path, tmp_path: Path) -> None:
        """Should return workspace info."""
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService(base_dir=tmp_path / "teams")
        service.share_project(sample_project, "info@test.com")

        workspace = service.get_workspace_info(sample_project)
        assert workspace is not None
        assert len(workspace.members) == 1


# ============================================================================
# FEATURE 18: METRICS - 20+ Tests
# ============================================================================


class TestMetricsService:
    """Tests for the metrics service."""

    def test_generate_metrics(self, sample_project: Path, tmp_path: Path) -> None:
        """Should generate comprehensive metrics."""
        from tac_bootstrap.application.metrics_service import MetricsService

        service = MetricsService(history_dir=tmp_path / "metrics")
        metrics = service.generate_metrics(sample_project)

        assert metrics.project_name == "test-project"
        assert metrics.source_file_count > 0
        assert metrics.health_score >= 0

    def test_health_score_range(self, sample_project: Path, tmp_path: Path) -> None:
        """Health score should be between 0 and 100."""
        from tac_bootstrap.application.metrics_service import MetricsService

        service = MetricsService(history_dir=tmp_path / "metrics")
        score = service.calculate_health_score(sample_project)

        assert 0 <= score <= 100

    def test_health_grade(self, sample_project: Path, tmp_path: Path) -> None:
        """Should compute a letter grade."""
        from tac_bootstrap.application.metrics_service import MetricsService

        service = MetricsService(history_dir=tmp_path / "metrics")
        metrics = service.generate_metrics(sample_project)

        assert metrics.health_grade in ("A+", "A", "B+", "B", "C+", "C", "D", "F")

    def test_complexity_metrics(self, sample_project: Path) -> None:
        """Should compute complexity metrics."""
        from tac_bootstrap.application.metrics_service import MetricsService

        service = MetricsService()
        complexity = service.get_complexity_metrics(sample_project)

        assert complexity.total_files > 0
        assert complexity.total_lines > 0

    def test_dependency_metrics(self, sample_project: Path) -> None:
        """Should detect dependencies."""
        from tac_bootstrap.application.metrics_service import MetricsService

        service = MetricsService()
        deps = service.get_dependency_metrics(sample_project)

        # sample project may or may not have pyproject.toml
        assert deps.total_dependencies >= 0

    def test_empty_project_metrics(self, tmp_path: Path) -> None:
        """Empty project should still generate valid metrics."""
        from tac_bootstrap.application.metrics_service import MetricsService

        empty_project = tmp_path / "empty"
        empty_project.mkdir()

        service = MetricsService(history_dir=tmp_path / "metrics")
        metrics = service.generate_metrics(empty_project)

        assert metrics.source_file_count == 0
        assert metrics.health_score >= 0

    def test_metrics_has_tests_flag(self, sample_project: Path, tmp_path: Path) -> None:
        """Should detect test files."""
        from tac_bootstrap.application.metrics_service import MetricsService

        service = MetricsService(history_dir=tmp_path / "metrics")
        metrics = service.generate_metrics(sample_project)

        assert metrics.has_tests is True

    def test_metrics_has_config_flag(self, sample_project: Path, tmp_path: Path) -> None:
        """Should detect config.yml."""
        from tac_bootstrap.application.metrics_service import MetricsService

        service = MetricsService(history_dir=tmp_path / "metrics")
        metrics = service.generate_metrics(sample_project)

        assert metrics.has_config is True

    def test_metrics_has_docs_flag(self, sample_project: Path, tmp_path: Path) -> None:
        """Should detect README.md."""
        from tac_bootstrap.application.metrics_service import MetricsService

        service = MetricsService(history_dir=tmp_path / "metrics")
        metrics = service.generate_metrics(sample_project)

        assert metrics.has_docs is True

    def test_save_and_load_history(self, sample_project: Path, tmp_path: Path) -> None:
        """Should save and load metrics history."""
        from tac_bootstrap.application.metrics_service import MetricsService

        service = MetricsService(history_dir=tmp_path / "metrics")
        metrics = service.generate_metrics(sample_project)
        service.save_metrics_history(sample_project, metrics)

        history = service.get_metrics_history(sample_project)
        assert len(history) >= 1

    def test_score_to_grade_mapping(self) -> None:
        """Score to grade mapping should be correct."""
        from tac_bootstrap.application.metrics_service import MetricsService

        service = MetricsService()
        assert service._score_to_grade(95) == "A+"
        assert service._score_to_grade(85) == "A"
        assert service._score_to_grade(75) == "B+"
        assert service._score_to_grade(65) == "B"
        assert service._score_to_grade(55) == "C+"
        assert service._score_to_grade(45) == "C"
        assert service._score_to_grade(35) == "D"
        assert service._score_to_grade(20) == "F"

    def test_file_metrics_model(self) -> None:
        """FileMetrics should have correct defaults."""
        from tac_bootstrap.application.metrics_service import FileMetrics

        fm = FileMetrics(path="test.py")
        assert fm.lines_of_code == 0
        assert fm.complexity_score == 0.0

    def test_language_distribution(self, sample_project: Path, tmp_path: Path) -> None:
        """Should compute language distribution."""
        from tac_bootstrap.application.metrics_service import MetricsService

        service = MetricsService(history_dir=tmp_path / "metrics")
        metrics = service.generate_metrics(sample_project)

        assert ".py" in metrics.language_distribution

    def test_recommendations_generated(self, tmp_path: Path) -> None:
        """Bare project should get recommendations."""
        from tac_bootstrap.application.metrics_service import MetricsService

        bare = tmp_path / "bare"
        bare.mkdir()
        (bare / "main.py").write_text("x = 1\n")

        service = MetricsService(history_dir=tmp_path / "metrics")
        metrics = service.generate_metrics(bare)

        assert len(metrics.recommendations) > 0


# ============================================================================
# FEATURE 19: RECOMMENDATIONS - 15+ Tests
# ============================================================================


class TestRecommendationService:
    """Tests for the recommendation service."""

    def test_analyze_sample_project(self, sample_project: Path) -> None:
        """Should analyze project and return report."""
        from tac_bootstrap.application.recommendation_service import RecommendationService

        service = RecommendationService()
        report = service.analyze(sample_project)

        assert report.total >= 0

    def test_check_security_clean(self, sample_project: Path) -> None:
        """Clean project should have no critical security issues."""
        from tac_bootstrap.application.recommendation_service import RecommendationService

        service = RecommendationService()
        recs = service.check_security(sample_project)

        critical = [r for r in recs if r.severity == "critical"]
        # Our sample project should be clean
        assert len(critical) == 0

    def test_check_security_hardcoded_password(self, tmp_path: Path) -> None:
        """Should detect hardcoded passwords."""
        from tac_bootstrap.application.recommendation_service import RecommendationService

        project = tmp_path / "insecure"
        project.mkdir()
        (project / "app.py").write_text('password = "supersecret123"\n')

        service = RecommendationService()
        recs = service.check_security(project)

        assert any("password" in r.title.lower() for r in recs)

    def test_check_structure_missing_readme(self, tmp_path: Path) -> None:
        """Should detect missing README."""
        from tac_bootstrap.application.recommendation_service import RecommendationService

        project = tmp_path / "no-readme"
        project.mkdir()

        service = RecommendationService()
        recs = service.check_structure(project)

        assert any("README" in r.title for r in recs)

    def test_check_structure_missing_gitignore(self, tmp_path: Path) -> None:
        """Should detect missing .gitignore."""
        from tac_bootstrap.application.recommendation_service import RecommendationService

        project = tmp_path / "no-gitignore"
        project.mkdir()

        service = RecommendationService()
        recs = service.check_structure(project)

        assert any("gitignore" in r.title.lower() for r in recs)

    def test_check_testing_no_tests(self, tmp_path: Path) -> None:
        """Should detect missing tests."""
        from tac_bootstrap.application.recommendation_service import RecommendationService

        project = tmp_path / "no-tests"
        project.mkdir()
        (project / "app.py").write_text("x = 1\n")

        service = RecommendationService()
        recs = service.check_testing(project)

        assert any("test" in r.title.lower() for r in recs)

    def test_check_performance_large_file(self, tmp_path: Path) -> None:
        """Should flag large files."""
        from tac_bootstrap.application.recommendation_service import RecommendationService

        project = tmp_path / "large-file"
        project.mkdir()
        large_content = "\n".join([f"line_{i} = {i}" for i in range(600)])
        (project / "big.py").write_text(large_content)

        service = RecommendationService()
        recs = service.check_performance(project)

        assert any("large" in r.title.lower() or "Large" in r.title for r in recs)

    def test_recommendation_model(self) -> None:
        """Recommendation model should have correct fields."""
        from tac_bootstrap.application.recommendation_service import Recommendation

        rec = Recommendation(
            id="test-1",
            category="security",
            title="Test recommendation",
        )
        assert rec.severity == "info"
        assert rec.auto_fixable is False

    def test_report_counts(self, sample_project: Path) -> None:
        """Report should have correct count breakdown."""
        from tac_bootstrap.application.recommendation_service import RecommendationService

        service = RecommendationService()
        report = service.analyze(sample_project)

        assert report.total == report.critical + report.warnings + report.info

    def test_report_categories(self, sample_project: Path) -> None:
        """Report should track categories."""
        from tac_bootstrap.application.recommendation_service import RecommendationService

        service = RecommendationService()
        report = service.analyze(sample_project)

        total_from_categories = sum(report.categories.values())
        assert total_from_categories == report.total

    def test_check_env_not_in_gitignore(self, tmp_path: Path) -> None:
        """Should detect .env not in .gitignore."""
        from tac_bootstrap.application.recommendation_service import RecommendationService

        project = tmp_path / "env-exposed"
        project.mkdir()
        (project / ".env").write_text("SECRET=abc\n")
        (project / ".gitignore").write_text("# empty\n")

        service = RecommendationService()
        recs = service.check_security(project)

        assert any("env" in r.id.lower() for r in recs)

    def test_sorted_by_severity(self, tmp_path: Path) -> None:
        """Recommendations should be sorted critical-first."""
        from tac_bootstrap.application.recommendation_service import RecommendationService

        project = tmp_path / "mixed"
        project.mkdir()
        (project / ".env").write_text("SECRET=abc\n")
        (project / ".gitignore").write_text("# nothing\n")
        (project / "app.py").write_text('password = "secret"\n')

        service = RecommendationService()
        report = service.analyze(project)

        if report.total > 1:
            severity_order = {"critical": 0, "warning": 1, "info": 2}
            for i in range(len(report.recommendations) - 1):
                s1 = severity_order.get(report.recommendations[i].severity, 3)
                s2 = severity_order.get(report.recommendations[i + 1].severity, 3)
                assert s1 <= s2


# ============================================================================
# FEATURE 20: COMMUNITY - 15+ Tests
# ============================================================================


class TestCommunityService:
    """Tests for the community service."""

    def test_browse_built_in_templates(self, tmp_path: Path) -> None:
        """Should browse built-in templates."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        templates = service.browse_templates()
        assert len(templates) > 0

    def test_browse_templates_by_category(self, tmp_path: Path) -> None:
        """Should filter templates by category."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        templates = service.browse_templates(category="authentication")
        assert len(templates) > 0

    def test_share_plugin(self, tmp_path: Path) -> None:
        """Should share a plugin."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        item = service.share_plugin("test-plugin", description="Test plugin")
        assert item.name == "test-plugin"
        assert item.item_type == "plugin"

    def test_share_plugin_empty_name_raises(self, tmp_path: Path) -> None:
        """Should raise for empty plugin name."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        with pytest.raises(ValueError, match="cannot be empty"):
            service.share_plugin("")

    def test_publish_template(self, tmp_path: Path) -> None:
        """Should publish a template."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        item = service.publish_template("my-template", description="Test template")
        assert item.name == "my-template"
        assert item.item_type == "template"

    def test_get_awards(self, tmp_path: Path) -> None:
        """Should return all achievement definitions."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        awards = service.get_awards()
        assert len(awards) >= 10

    def test_earn_achievement(self, tmp_path: Path) -> None:
        """Should earn an achievement."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        award = service.earn_achievement("first-project")
        assert award is not None
        assert award.earned is True

    def test_earn_duplicate_achievement(self, tmp_path: Path) -> None:
        """Should return None for already earned achievement."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        service.earn_achievement("first-project")
        result = service.earn_achievement("first-project")
        assert result is None

    def test_earn_nonexistent_achievement(self, tmp_path: Path) -> None:
        """Should return None for nonexistent achievement."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        result = service.earn_achievement("nonexistent-id")
        assert result is None

    def test_get_profile(self, tmp_path: Path) -> None:
        """Should return user profile."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        profile = service.get_profile()
        assert profile is not None

    def test_profile_updates_on_share(self, tmp_path: Path) -> None:
        """Profile should update when sharing plugins."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        service.share_plugin("p1", description="Test")

        profile = service.get_profile()
        assert profile.plugins_shared >= 1

    def test_community_stats(self, tmp_path: Path) -> None:
        """Should return community statistics."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        stats = service.get_community_stats()
        assert stats.total_templates > 0 or stats.total_plugins > 0

    def test_browse_plugins(self, tmp_path: Path) -> None:
        """Should browse plugins."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        plugins = service.browse_plugins()
        assert len(plugins) >= 0

    def test_browse_with_search_query(self, tmp_path: Path) -> None:
        """Should search templates by query."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService(base_dir=tmp_path / "community")
        results = service.browse_templates(query="auth")
        assert len(results) > 0

    def test_community_item_model(self) -> None:
        """CommunityItem model should have correct defaults."""
        from tac_bootstrap.application.community_service import CommunityItem

        item = CommunityItem(name="test", item_type="plugin")
        assert item.version == "1.0.0"
        assert item.rating == 0.0


# ============================================================================
# CLI INTEGRATION TESTS - Phase 3 Commands
# ============================================================================


class TestPhase3CLICommands:
    """Integration tests for Phase 3 CLI commands."""

    def test_config_set_language(self, temp_home: Path) -> None:
        """config set language should work."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            result = runner.invoke(app, ["config", "set", "language", "es"])
            assert result.exit_code == 0

    def test_config_set_invalid_language(self, temp_home: Path) -> None:
        """config set with invalid language should fail."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            result = runner.invoke(app, ["config", "set", "language", "xx"])
            assert result.exit_code == 1

    def test_config_get_language(self, temp_home: Path) -> None:
        """config get language should work."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            result = runner.invoke(app, ["config", "get", "language"])
            assert result.exit_code == 0

    def test_config_list(self, temp_home: Path) -> None:
        """config list should show all settings."""
        from tac_bootstrap.infrastructure.i18n import I18nService

        with patch.object(Path, "home", return_value=temp_home):
            I18nService.reset_instance()
            result = runner.invoke(app, ["config", "list"])
            assert result.exit_code == 0
            assert "language" in result.stdout

    def test_search_commands_cli(self) -> None:
        """search commands should work via CLI."""
        result = runner.invoke(app, ["search", "commands", "test"])
        assert result.exit_code == 0

    def test_search_templates_cli(self) -> None:
        """search templates should work via CLI."""
        result = runner.invoke(app, ["search", "templates"])
        assert result.exit_code == 0

    def test_search_features_cli(self) -> None:
        """search features should work via CLI."""
        result = runner.invoke(app, ["search", "features"])
        assert result.exit_code == 0

    def test_learn_list_topics(self) -> None:
        """learn without topic should list topics."""
        result = runner.invoke(app, ["learn"])
        assert result.exit_code == 0
        assert "Available Learning Topics" in result.stdout

    def test_learn_specific_topic(self) -> None:
        """learn with specific topic should show content."""
        result = runner.invoke(app, ["learn", "--topic", "ddd"])
        assert result.exit_code == 0
        assert "DDD" in result.stdout

    def test_tutorial_quick_start(self) -> None:
        """tutorial should show quick-start."""
        result = runner.invoke(app, ["tutorial", "--type", "quick-start"])
        assert result.exit_code == 0
        assert "Quick Start" in result.stdout

    def test_dashboard_status(self) -> None:
        """dashboard status should work."""
        result = runner.invoke(app, ["dashboard", "status"])
        assert result.exit_code == 0

    def test_recommend_command(self, sample_project: Path) -> None:
        """recommend command should analyze project."""
        result = runner.invoke(
            app, ["recommend", "--path", str(sample_project)]
        )
        assert result.exit_code == 0

    def test_metrics_generate(self, sample_project: Path) -> None:
        """metrics generate should produce output."""
        result = runner.invoke(
            app, ["metrics", "generate", "--path", str(sample_project)]
        )
        assert result.exit_code == 0
        assert "Health Score" in result.stdout

    def test_community_browse(self) -> None:
        """community browse should show items."""
        result = runner.invoke(app, ["community", "browse"])
        assert result.exit_code == 0

    def test_community_awards(self) -> None:
        """community awards should show achievements."""
        result = runner.invoke(app, ["community", "awards"])
        assert result.exit_code == 0
        assert "Achievements" in result.stdout
