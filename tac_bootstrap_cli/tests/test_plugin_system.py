"""Tests for the Plugin System (Feature 5).

Comprehensive test suite covering plugin domain models, plugin loader,
plugin service, hook execution, error handling, and edge cases.
"""

import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest
import yaml

from tac_bootstrap.domain.plugin import (
    HookType,
    Plugin,
    PluginHookResult,
    PluginManifest,
)
from tac_bootstrap.infrastructure.plugin_loader import (
    PluginLoader,
    PluginLoadError,
    PluginManifestError,
)
from tac_bootstrap.application.plugin_service import PluginService


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def valid_manifest_data() -> Dict[str, Any]:
    """Valid plugin manifest data."""
    return {
        "name": "test-plugin",
        "version": "1.0.0",
        "author": "Test Author",
        "description": "A test plugin",
        "hooks": ["post_project_create", "pre_scaffold"],
        "dependencies": [],
        "config": {"key": "value"},
    }


@pytest.fixture
def valid_manifest(valid_manifest_data: Dict[str, Any]) -> PluginManifest:
    """Create a valid PluginManifest instance."""
    return PluginManifest(**valid_manifest_data)


@pytest.fixture
def plugin_dir(tmp_path: Path, valid_manifest_data: Dict[str, Any]) -> Path:
    """Create a temporary plugin directory with manifest and hooks."""
    plugin_path = tmp_path / "test-plugin"
    plugin_path.mkdir()

    # Write manifest
    manifest_path = plugin_path / "plugin.yaml"
    with open(manifest_path, "w") as f:
        yaml.dump(valid_manifest_data, f)

    # Write hooks.py
    hooks_path = plugin_path / "hooks.py"
    hooks_path.write_text(
        '''
def post_project_create(*args, **kwargs):
    return {"action": "post_create", "status": "ok"}

def pre_scaffold(*args, **kwargs):
    return {"action": "pre_scaffold", "status": "ok"}
'''
    )

    return plugin_path


@pytest.fixture
def plugins_dir(tmp_path: Path, valid_manifest_data: Dict[str, Any]) -> Path:
    """Create a plugins directory with multiple plugin subdirectories."""
    plugins_path = tmp_path / "plugins"
    plugins_path.mkdir()

    # Plugin 1
    p1 = plugins_path / "plugin-one"
    p1.mkdir()
    data1 = valid_manifest_data.copy()
    data1["name"] = "plugin-one"
    with open(p1 / "plugin.yaml", "w") as f:
        yaml.dump(data1, f)
    (p1 / "hooks.py").write_text(
        'def post_project_create(**kwargs): return {"source": "plugin-one"}\n'
    )

    # Plugin 2
    p2 = plugins_path / "plugin-two"
    p2.mkdir()
    data2 = valid_manifest_data.copy()
    data2["name"] = "plugin-two"
    data2["hooks"] = ["post_scaffold"]
    with open(p2 / "plugin.yaml", "w") as f:
        yaml.dump(data2, f)
    (p2 / "hooks.py").write_text(
        'def post_scaffold(**kwargs): return {"source": "plugin-two"}\n'
    )

    return plugins_path


@pytest.fixture
def loader() -> PluginLoader:
    """Create a PluginLoader instance."""
    return PluginLoader()


@pytest.fixture
def service() -> PluginService:
    """Create a PluginService instance."""
    return PluginService()


# ============================================================================
# TEST PLUGIN MANIFEST
# ============================================================================


class TestPluginManifest:
    """Tests for PluginManifest Pydantic model."""

    def test_valid_manifest(self, valid_manifest_data: Dict[str, Any]):
        """Valid manifest data should create a PluginManifest."""
        manifest = PluginManifest(**valid_manifest_data)
        assert manifest.name == "test-plugin"
        assert manifest.version == "1.0.0"
        assert manifest.author == "Test Author"

    def test_manifest_empty_name_raises(self):
        """Empty name should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            PluginManifest(name="", version="1.0.0", author="Test")

    def test_manifest_invalid_name_format(self):
        """Invalid name format should raise ValueError."""
        with pytest.raises(ValueError, match="must be lowercase-hyphen"):
            PluginManifest(name="InvalidName", version="1.0.0", author="Test")

    def test_manifest_invalid_version(self):
        """Invalid version should raise ValueError."""
        with pytest.raises(ValueError, match="semantic versioning"):
            PluginManifest(name="test", version="bad", author="Test")

    def test_manifest_valid_version_formats(self):
        """Various valid version formats should work."""
        for version in ["1.0", "1.0.0", "1.0.0-beta", "0.1.0-rc.1"]:
            m = PluginManifest(name="test", version=version, author="Test")
            assert m.version == version

    def test_manifest_invalid_hook(self):
        """Invalid hook name should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid hook"):
            PluginManifest(
                name="test", version="1.0.0", author="Test",
                hooks=["invalid_hook_name"]
            )

    def test_manifest_valid_hooks(self):
        """All valid hook types should be accepted."""
        hooks = [h.value for h in HookType]
        m = PluginManifest(name="test", version="1.0.0", author="Test", hooks=hooks)
        assert len(m.hooks) == len(HookType)

    def test_manifest_defaults(self):
        """Default values should be applied."""
        m = PluginManifest(name="test", version="1.0.0", author="Test")
        assert m.description == ""
        assert m.hooks == []
        assert m.dependencies == []
        assert m.config == {}


# ============================================================================
# TEST PLUGIN
# ============================================================================


class TestPlugin:
    """Tests for Plugin runtime model."""

    def test_plugin_creation(self, valid_manifest: PluginManifest):
        """Plugin should be created from manifest."""
        plugin = Plugin(manifest=valid_manifest)
        assert plugin.name == "test-plugin"
        assert plugin.version == "1.0.0"
        assert plugin.author == "Test Author"
        assert plugin.enabled is True

    def test_plugin_has_hook(self, valid_manifest: PluginManifest):
        """has_hook should detect registered hooks."""
        hooks = {"post_project_create": lambda: None}
        plugin = Plugin(manifest=valid_manifest, hooks=hooks)
        assert plugin.has_hook("post_project_create") is True
        assert plugin.has_hook("on_error") is False

    def test_plugin_execute_hook_success(self, valid_manifest: PluginManifest):
        """Hook execution should return success result."""
        hooks = {"post_project_create": lambda **kw: {"status": "ok"}}
        plugin = Plugin(manifest=valid_manifest, hooks=hooks)
        result = plugin.execute_hook("post_project_create")
        assert result.success is True
        assert result.data == {"status": "ok"}

    def test_plugin_execute_hook_disabled(self, valid_manifest: PluginManifest):
        """Disabled plugins should not execute hooks."""
        hooks = {"post_project_create": lambda: None}
        plugin = Plugin(manifest=valid_manifest, hooks=hooks, enabled=False)
        result = plugin.execute_hook("post_project_create")
        assert result.success is False
        assert "disabled" in result.message

    def test_plugin_execute_hook_not_implemented(self, valid_manifest: PluginManifest):
        """Executing missing hook should return failure result."""
        plugin = Plugin(manifest=valid_manifest)
        result = plugin.execute_hook("on_error")
        assert result.success is False
        assert "not implemented" in result.message

    def test_plugin_execute_hook_error(self, valid_manifest: PluginManifest):
        """Hook that raises should return failure result."""
        def bad_hook(**kwargs: Any) -> None:
            raise RuntimeError("hook failed")

        hooks = {"on_error": bad_hook}
        plugin = Plugin(manifest=valid_manifest, hooks=hooks)
        result = plugin.execute_hook("on_error")
        assert result.success is False
        assert "failed" in result.message

    def test_plugin_repr(self, valid_manifest: PluginManifest):
        """Plugin repr should show name, version, and status."""
        plugin = Plugin(manifest=valid_manifest)
        r = repr(plugin)
        assert "test-plugin" in r
        assert "1.0.0" in r
        assert "enabled" in r

    def test_plugin_disabled_repr(self, valid_manifest: PluginManifest):
        """Disabled plugin repr should show disabled status."""
        plugin = Plugin(manifest=valid_manifest, enabled=False)
        assert "disabled" in repr(plugin)


# ============================================================================
# TEST PLUGIN LOADER
# ============================================================================


class TestPluginLoader:
    """Tests for PluginLoader filesystem operations."""

    def test_discover_plugins(self, plugins_dir: Path, loader: PluginLoader):
        """Loader should discover plugin directories."""
        dirs = loader.discover_plugins(plugins_dir)
        assert len(dirs) == 2

    def test_discover_plugins_empty_dir(self, tmp_path: Path, loader: PluginLoader):
        """Empty directory should return no plugins."""
        dirs = loader.discover_plugins(tmp_path)
        assert dirs == []

    def test_discover_plugins_nonexistent(self, loader: PluginLoader):
        """Non-existent directory should return empty list."""
        dirs = loader.discover_plugins(Path("/nonexistent"))
        assert dirs == []

    def test_load_manifest(self, plugin_dir: Path, loader: PluginLoader):
        """Loader should parse plugin.yaml into PluginManifest."""
        manifest = loader.load_manifest(plugin_dir)
        assert manifest.name == "test-plugin"
        assert manifest.version == "1.0.0"

    def test_load_manifest_missing(self, tmp_path: Path, loader: PluginLoader):
        """Missing manifest should raise PluginManifestError."""
        with pytest.raises(PluginManifestError):
            loader.load_manifest(tmp_path)

    def test_load_manifest_invalid_yaml(self, tmp_path: Path, loader: PluginLoader):
        """Invalid YAML should raise PluginManifestError."""
        (tmp_path / "plugin.yaml").write_text("{{invalid yaml")
        with pytest.raises(PluginManifestError):
            loader.load_manifest(tmp_path)

    def test_load_manifest_yml_extension(self, tmp_path: Path, loader: PluginLoader):
        """plugin.yml should be accepted as alternative."""
        plugin_dir = tmp_path / "alt-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "plugin.yml").write_text(
            yaml.dump({"name": "alt-plugin", "version": "1.0.0", "author": "Test"})
        )
        manifest = loader.load_manifest(plugin_dir)
        assert manifest.name == "alt-plugin"

    def test_load_hooks(self, plugin_dir: Path, loader: PluginLoader):
        """Loader should dynamically import hooks from hooks.py."""
        hooks = loader.load_hooks(plugin_dir)
        assert "post_project_create" in hooks
        assert "pre_scaffold" in hooks
        assert callable(hooks["post_project_create"])

    def test_load_hooks_no_file(self, tmp_path: Path, loader: PluginLoader):
        """Missing hooks.py should return empty dict."""
        hooks = loader.load_hooks(tmp_path)
        assert hooks == {}

    def test_load_plugin_complete(self, plugin_dir: Path, loader: PluginLoader):
        """Full plugin load should succeed with manifest and hooks."""
        plugin = loader.load_plugin(plugin_dir)
        assert plugin.enabled is True
        assert plugin.name == "test-plugin"
        assert plugin.has_hook("post_project_create")

    def test_load_plugin_bad_manifest(self, tmp_path: Path, loader: PluginLoader):
        """Bad manifest should produce disabled plugin."""
        bad_dir = tmp_path / "bad-plugin"
        bad_dir.mkdir()
        (bad_dir / "plugin.yaml").write_text("not: valid: manifest: data:")
        plugin = loader.load_plugin(bad_dir)
        assert plugin.enabled is False
        assert plugin.load_error is not None

    def test_load_all(self, plugins_dir: Path, loader: PluginLoader):
        """load_all should return all plugins in directory."""
        plugins = loader.load_all(plugins_dir)
        assert len(plugins) == 2
        names = {p.name for p in plugins}
        assert "plugin-one" in names
        assert "plugin-two" in names

    def test_validate_dependencies_satisfied(self, loader: PluginLoader):
        """Satisfied dependencies should return no errors."""
        m1 = PluginManifest(name="dep-a", version="1.0.0", author="Test")
        m2 = PluginManifest(
            name="dep-b", version="1.0.0", author="Test",
            dependencies=["dep-a"]
        )
        p1 = Plugin(manifest=m1)
        p2 = Plugin(manifest=m2)
        errors = loader.validate_dependencies([p1, p2])
        assert errors == []

    def test_validate_dependencies_unsatisfied(self, loader: PluginLoader):
        """Unsatisfied dependencies should return error messages."""
        m = PluginManifest(
            name="needs-dep", version="1.0.0", author="Test",
            dependencies=["missing-plugin"]
        )
        p = Plugin(manifest=m)
        errors = loader.validate_dependencies([p])
        assert len(errors) == 1
        assert "missing-plugin" in errors[0]


# ============================================================================
# TEST PLUGIN SERVICE
# ============================================================================


class TestPluginService:
    """Tests for PluginService orchestration."""

    def test_load_plugins(self, plugins_dir: Path, service: PluginService):
        """Service should load plugins from directory."""
        loaded = service.load_plugins(plugins_dir)
        assert len(loaded) == 2
        assert service.plugin_count == 2

    def test_register_plugin(self, service: PluginService, valid_manifest: PluginManifest):
        """Manual plugin registration should work."""
        plugin = Plugin(manifest=valid_manifest)
        service.register_plugin(plugin)
        assert service.plugin_count == 1
        assert service.get_plugin("test-plugin") is not None

    def test_register_plugin_duplicate(self, service: PluginService, valid_manifest: PluginManifest):
        """Registering duplicate should replace existing."""
        p1 = Plugin(manifest=valid_manifest)
        p2 = Plugin(manifest=valid_manifest, enabled=False)
        service.register_plugin(p1)
        service.register_plugin(p2)
        assert service.plugin_count == 1
        assert service.get_plugin("test-plugin").enabled is False

    def test_unregister_plugin(self, service: PluginService, valid_manifest: PluginManifest):
        """Unregistering should remove plugin."""
        plugin = Plugin(manifest=valid_manifest)
        service.register_plugin(plugin)
        assert service.unregister_plugin("test-plugin") is True
        assert service.plugin_count == 0

    def test_unregister_nonexistent(self, service: PluginService):
        """Unregistering nonexistent should return False."""
        assert service.unregister_plugin("nonexistent") is False

    def test_register_hook(self, service: PluginService):
        """Standalone hook registration should work."""
        callback = lambda **kw: {"custom": True}
        service.register_hook("post_project_create", callback)

    def test_register_invalid_hook(self, service: PluginService):
        """Invalid hook name should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid hook name"):
            service.register_hook("invalid_hook", lambda: None)

    def test_execute_hook(self, service: PluginService, valid_manifest: PluginManifest):
        """Hook execution should reach all plugins with that hook."""
        hooks = {"post_project_create": lambda **kw: {"result": "ok"}}
        plugin = Plugin(manifest=valid_manifest, hooks=hooks)
        service.register_plugin(plugin)

        results = service.execute_hook("post_project_create")
        assert len(results) == 1
        assert results[0].success is True

    def test_execute_hook_with_custom_callback(self, service: PluginService):
        """Custom callbacks should also execute."""
        service.register_hook(
            "on_command",
            lambda **kw: {"custom": True}
        )
        results = service.execute_hook("on_command")
        assert len(results) == 1
        assert results[0].plugin_name == "custom"

    def test_execute_hook_error_isolation(self, service: PluginService):
        """Error in one plugin should not block others."""
        m1 = PluginManifest(name="plugin-a", version="1.0.0", author="Test")
        m2 = PluginManifest(name="plugin-b", version="1.0.0", author="Test")

        def bad_hook(**kwargs: Any) -> None:
            raise RuntimeError("boom")

        p1 = Plugin(manifest=m1, hooks={"on_error": bad_hook})
        p2 = Plugin(manifest=m2, hooks={"on_error": lambda **kw: {"ok": True}})

        service.register_plugin(p1)
        service.register_plugin(p2)

        results = service.execute_hook("on_error")
        assert len(results) == 2
        assert results[0].success is False  # p1 failed
        assert results[1].success is True   # p2 succeeded

    def test_list_plugins(self, service: PluginService, valid_manifest: PluginManifest):
        """list_plugins should return all plugins."""
        p = Plugin(manifest=valid_manifest)
        service.register_plugin(p)
        assert len(service.list_plugins()) == 1

    def test_get_enabled_disabled(self, service: PluginService):
        """get_enabled_plugins and get_disabled_plugins should filter correctly."""
        m1 = PluginManifest(name="enabled-p", version="1.0.0", author="Test")
        m2 = PluginManifest(name="disabled-p", version="1.0.0", author="Test")

        service.register_plugin(Plugin(manifest=m1, enabled=True))
        service.register_plugin(Plugin(manifest=m2, enabled=False))

        assert len(service.get_enabled_plugins()) == 1
        assert len(service.get_disabled_plugins()) == 1
        assert service.enabled_count == 1

    def test_enable_disable_plugin(self, service: PluginService, valid_manifest: PluginManifest):
        """Enable and disable should toggle plugin state."""
        p = Plugin(manifest=valid_manifest, enabled=True)
        service.register_plugin(p)

        assert service.disable_plugin("test-plugin") is True
        assert service.get_plugin("test-plugin").enabled is False

        assert service.enable_plugin("test-plugin") is True
        assert service.get_plugin("test-plugin").enabled is True

    def test_enable_nonexistent(self, service: PluginService):
        """Enable/disable nonexistent should return False."""
        assert service.enable_plugin("nope") is False
        assert service.disable_plugin("nope") is False

    def test_get_hooks_for_type(self, service: PluginService):
        """get_hooks_for_type should return plugin names implementing that hook."""
        m = PluginManifest(name="hook-test", version="1.0.0", author="Test")
        hooks = {"pre_scaffold": lambda **kw: None}
        service.register_plugin(Plugin(manifest=m, hooks=hooks))

        names = service.get_hooks_for_type("pre_scaffold")
        assert "hook-test" in names
        assert service.get_hooks_for_type("on_error") == []

    def test_clear(self, service: PluginService, valid_manifest: PluginManifest):
        """clear should remove all plugins and hooks."""
        service.register_plugin(Plugin(manifest=valid_manifest))
        service.register_hook("on_command", lambda: None)
        service.clear()
        assert service.plugin_count == 0


# ============================================================================
# TEST HOOK TYPE ENUM
# ============================================================================


class TestHookType:
    """Tests for HookType enum."""

    def test_all_hook_types_exist(self):
        """All expected hook types should be defined."""
        expected = {
            "post_project_create", "pre_scaffold", "post_scaffold",
            "on_command", "on_error"
        }
        actual = {h.value for h in HookType}
        assert actual == expected

    def test_hook_type_values(self):
        """Hook type values should match their names."""
        assert HookType.POST_PROJECT_CREATE.value == "post_project_create"
        assert HookType.ON_ERROR.value == "on_error"


# ============================================================================
# TEST PLUGIN HOOK RESULT
# ============================================================================


class TestPluginHookResult:
    """Tests for PluginHookResult model."""

    def test_success_result(self):
        """Successful result should have correct fields."""
        result = PluginHookResult(
            plugin_name="test",
            hook_name="on_command",
            success=True,
            message="ok",
            data={"key": "value"},
        )
        assert result.success is True
        assert result.data["key"] == "value"

    def test_failure_result(self):
        """Failure result should capture error."""
        result = PluginHookResult(
            plugin_name="test",
            hook_name="on_error",
            success=False,
            message="something failed",
        )
        assert result.success is False
        assert "failed" in result.message

    def test_default_values(self):
        """Default values should be applied."""
        result = PluginHookResult(plugin_name="test", hook_name="on_command")
        assert result.success is True
        assert result.message == ""
        assert result.data == {}
