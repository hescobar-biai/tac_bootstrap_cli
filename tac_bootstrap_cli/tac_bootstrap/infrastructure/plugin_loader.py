"""
IDK: plugin-discovery, plugin-loading, dynamic-import, yaml-manifest-parsing
Responsibility: Discovers and loads plugins from filesystem directories, parses manifests,
                and dynamically imports hook implementations
Invariants: Plugin directories must contain plugin.yaml, hooks.py is optional,
            loading errors are captured gracefully without crashing
"""

import importlib.util
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List

import yaml

from tac_bootstrap.domain.plugin import (
    HookType,
    Plugin,
    PluginManifest,
)

# ============================================================================
# EXCEPTIONS
# ============================================================================


class PluginLoadError(Exception):
    """Raised when a plugin fails to load."""

    def __init__(self, plugin_name: str, reason: str) -> None:
        self.plugin_name = plugin_name
        self.reason = reason
        super().__init__(f"Failed to load plugin '{plugin_name}': {reason}")


class PluginManifestError(Exception):
    """Raised when a plugin manifest is invalid."""

    def __init__(self, manifest_path: str, reason: str) -> None:
        self.manifest_path = manifest_path
        self.reason = reason
        super().__init__(f"Invalid plugin manifest at '{manifest_path}': {reason}")


# ============================================================================
# PLUGIN LOADER
# ============================================================================


class PluginLoader:
    """
    IDK: plugin-filesystem-discovery, dynamic-module-loading, manifest-parsing
    Responsibility: Discovers plugin directories, parses plugin.yaml manifests,
                    dynamically loads hooks.py modules, and creates Plugin instances
    Invariants: Each plugin directory must have plugin.yaml, loading failures are
                captured as load_error on Plugin, no exceptions propagate on bad plugins
    """

    # Valid hook function names that map to HookType values
    VALID_HOOK_NAMES = {h.value for h in HookType}

    def discover_plugins(self, plugins_dir: Path) -> List[Path]:
        """
        Discover plugin directories within a parent directory.

        A valid plugin directory contains a plugin.yaml manifest file.

        Args:
            plugins_dir: Parent directory containing plugin subdirectories

        Returns:
            List of paths to valid plugin directories (sorted by name)
        """
        if not plugins_dir.is_dir():
            return []

        plugin_dirs = []
        for item in sorted(plugins_dir.iterdir()):
            if item.is_dir() and (item / "plugin.yaml").is_file():
                plugin_dirs.append(item)
            elif item.is_dir() and (item / "plugin.yml").is_file():
                plugin_dirs.append(item)

        return plugin_dirs

    def load_manifest(self, plugin_dir: Path) -> PluginManifest:
        """
        Load and validate a plugin manifest from a directory.

        Looks for plugin.yaml or plugin.yml in the specified directory.

        Args:
            plugin_dir: Path to the plugin directory

        Returns:
            Validated PluginManifest instance

        Raises:
            PluginManifestError: If manifest is missing, unreadable, or invalid
        """
        manifest_path = plugin_dir / "plugin.yaml"
        if not manifest_path.is_file():
            manifest_path = plugin_dir / "plugin.yml"

        if not manifest_path.is_file():
            raise PluginManifestError(
                str(plugin_dir), "No plugin.yaml or plugin.yml found"
            )

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                raw_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise PluginManifestError(str(manifest_path), f"YAML parse error: {e}")
        except OSError as e:
            raise PluginManifestError(str(manifest_path), f"File read error: {e}")

        if not isinstance(raw_data, dict):
            raise PluginManifestError(
                str(manifest_path), "Manifest must be a YAML mapping"
            )

        try:
            return PluginManifest(**raw_data)
        except Exception as e:
            raise PluginManifestError(str(manifest_path), f"Validation error: {e}")

    def load_hooks(self, plugin_dir: Path) -> Dict[str, Callable[..., Any]]:
        """
        Dynamically load hook implementations from a plugin's hooks.py.

        Scans for functions whose names match valid hook types.

        Args:
            plugin_dir: Path to the plugin directory

        Returns:
            Dictionary mapping hook names to callable implementations.
            Returns empty dict if hooks.py doesn't exist.

        Raises:
            PluginLoadError: If hooks.py exists but cannot be imported
        """
        hooks_file = plugin_dir / "hooks.py"
        if not hooks_file.is_file():
            return {}

        # Generate a unique module name to avoid collisions
        plugin_name = plugin_dir.name
        module_name = f"tac_plugin_{plugin_name}_hooks"

        try:
            spec = importlib.util.spec_from_file_location(module_name, str(hooks_file))
            if spec is None or spec.loader is None:
                raise PluginLoadError(plugin_name, "Cannot create module spec for hooks.py")

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # Discover hook functions
            hooks: Dict[str, Callable[..., Any]] = {}
            for hook_name in self.VALID_HOOK_NAMES:
                if hasattr(module, hook_name) and callable(getattr(module, hook_name)):
                    hooks[hook_name] = getattr(module, hook_name)

            return hooks

        except PluginLoadError:
            raise
        except Exception as e:
            raise PluginLoadError(plugin_name, f"Error importing hooks.py: {e}")

    def load_plugin(self, plugin_dir: Path) -> Plugin:
        """
        Load a single plugin from a directory.

        Loads the manifest and optionally the hooks module. If loading fails,
        returns a Plugin with enabled=False and the error captured in load_error.

        Args:
            plugin_dir: Path to the plugin directory

        Returns:
            Plugin instance (may be disabled if loading failed)
        """
        try:
            manifest = self.load_manifest(plugin_dir)
        except (PluginManifestError, Exception) as e:
            # Create a minimal manifest for error reporting
            return Plugin(
                manifest=PluginManifest(
                    name=plugin_dir.name,
                    version="0.0.0",
                    author="unknown",
                    description=f"Failed to load: {e}",
                ),
                enabled=False,
                load_error=str(e),
            )

        try:
            hooks = self.load_hooks(plugin_dir)
        except (PluginLoadError, Exception) as e:
            return Plugin(
                manifest=manifest,
                enabled=False,
                load_error=str(e),
            )

        return Plugin(manifest=manifest, hooks=hooks, enabled=True)

    def load_all(self, plugins_dir: Path) -> List[Plugin]:
        """
        Discover and load all plugins from a directory.

        Args:
            plugins_dir: Parent directory containing plugin subdirectories

        Returns:
            List of loaded Plugin instances (some may be disabled due to errors)
        """
        plugin_dirs = self.discover_plugins(plugins_dir)
        plugins: List[Plugin] = []

        for plugin_dir in plugin_dirs:
            plugin = self.load_plugin(plugin_dir)
            plugins.append(plugin)

        return plugins

    def validate_dependencies(self, plugins: List[Plugin]) -> List[str]:
        """
        Validate that all plugin dependencies are satisfied.

        Args:
            plugins: List of loaded plugins

        Returns:
            List of error messages for unsatisfied dependencies
        """
        available_names = {p.name for p in plugins if p.enabled}
        errors: List[str] = []

        for plugin in plugins:
            if not plugin.enabled:
                continue
            for dep in plugin.manifest.dependencies:
                if dep not in available_names:
                    errors.append(
                        f"Plugin '{plugin.name}' requires '{dep}' which is not available"
                    )

        return errors
