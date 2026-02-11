"""
IDK: plugin-orchestration, hook-execution, plugin-lifecycle, plugin-registry
Responsibility: Orchestrates plugin loading, registration, hook execution, and lifecycle management
Invariants: Hooks execute in registration order, errors in one plugin don't block others,
            disabled plugins are skipped, hook results are always returned
"""

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from tac_bootstrap.domain.plugin import (
    HookType,
    Plugin,
    PluginHookResult,
)
from tac_bootstrap.infrastructure.plugin_loader import PluginLoader

# ============================================================================
# PLUGIN SERVICE
# ============================================================================


class PluginService:
    """
    IDK: plugin-lifecycle-manager, hook-registry, hook-dispatcher
    Responsibility: Manages plugin loading, registration, hook execution, and plugin queries
    Invariants: Hooks execute in registration order, one plugin's error never blocks others,
                disabled plugins are always skipped, all results are collected and returned
    """

    def __init__(self, loader: Optional[PluginLoader] = None) -> None:
        """
        Initialize PluginService.

        Args:
            loader: Optional PluginLoader instance (created if not provided)
        """
        self.loader = loader or PluginLoader()
        self._plugins: List[Plugin] = []
        self._custom_hooks: Dict[str, List[Callable[..., Any]]] = {}

    # ========================================================================
    # PLUGIN LOADING
    # ========================================================================

    def load_plugins(self, plugins_dir: Path) -> List[Plugin]:
        """
        Load all plugins from a directory.

        Discovers, loads, and validates all plugins in the given directory.
        Plugins that fail to load are included with enabled=False and an error message.

        Args:
            plugins_dir: Directory containing plugin subdirectories

        Returns:
            List of loaded Plugin instances
        """
        loaded = self.loader.load_all(plugins_dir)

        # Validate dependencies
        dep_errors = self.loader.validate_dependencies(loaded)
        if dep_errors:
            # Disable plugins with unmet dependencies
            unmet_deps = set()
            for error_msg in dep_errors:
                # Extract plugin name from error message
                for plugin in loaded:
                    if plugin.name in error_msg and "requires" in error_msg:
                        plugin.enabled = False
                        plugin.load_error = error_msg
                        unmet_deps.add(plugin.name)

        self._plugins.extend(loaded)
        return loaded

    def register_plugin(self, plugin: Plugin) -> None:
        """
        Manually register a plugin instance.

        Args:
            plugin: Plugin instance to register
        """
        # Avoid duplicate registrations
        existing_names = {p.name for p in self._plugins}
        if plugin.name in existing_names:
            # Replace existing plugin
            self._plugins = [p for p in self._plugins if p.name != plugin.name]

        self._plugins.append(plugin)

    def unregister_plugin(self, plugin_name: str) -> bool:
        """
        Remove a plugin from the registry.

        Args:
            plugin_name: Name of the plugin to remove

        Returns:
            True if plugin was found and removed, False otherwise
        """
        original_count = len(self._plugins)
        self._plugins = [p for p in self._plugins if p.name != plugin_name]
        return len(self._plugins) < original_count

    # ========================================================================
    # HOOK REGISTRATION
    # ========================================================================

    def register_hook(self, hook_name: str, callback: Callable[..., Any]) -> None:
        """
        Register a standalone hook callback (not associated with a plugin).

        Args:
            hook_name: Name of the hook to register for
            callback: Callable to invoke when hook is triggered

        Raises:
            ValueError: If hook_name is not a valid hook type
        """
        valid_hooks = {h.value for h in HookType}
        if hook_name not in valid_hooks:
            raise ValueError(
                f"Invalid hook name '{hook_name}'. "
                f"Valid hooks: {', '.join(sorted(valid_hooks))}"
            )

        if hook_name not in self._custom_hooks:
            self._custom_hooks[hook_name] = []

        self._custom_hooks[hook_name].append(callback)

    # ========================================================================
    # HOOK EXECUTION
    # ========================================================================

    def execute_hook(
        self,
        hook_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> List[PluginHookResult]:
        """
        Execute a hook across all registered plugins and custom callbacks.

        Executes hooks in registration order. Errors in one plugin do not
        prevent execution in subsequent plugins.

        Args:
            hook_name: Name of the hook to execute
            *args: Positional arguments to pass to hook implementations
            **kwargs: Keyword arguments to pass to hook implementations

        Returns:
            List of PluginHookResult from each plugin that handled the hook
        """
        results: List[PluginHookResult] = []

        # Execute plugin hooks first
        for plugin in self._plugins:
            if not plugin.enabled:
                continue
            if plugin.has_hook(hook_name):
                result = plugin.execute_hook(hook_name, *args, **kwargs)
                results.append(result)

        # Execute custom (standalone) hooks
        if hook_name in self._custom_hooks:
            for callback in self._custom_hooks[hook_name]:
                try:
                    cb_result = callback(*args, **kwargs)
                    data = cb_result if isinstance(cb_result, dict) else {}
                    results.append(
                        PluginHookResult(
                            plugin_name="custom",
                            hook_name=hook_name,
                            success=True,
                            message="Custom hook executed successfully",
                            data=data,
                        )
                    )
                except Exception as e:
                    results.append(
                        PluginHookResult(
                            plugin_name="custom",
                            hook_name=hook_name,
                            success=False,
                            message=f"Custom hook failed: {str(e)}",
                        )
                    )

        return results

    # ========================================================================
    # PLUGIN QUERIES
    # ========================================================================

    def list_plugins(self) -> List[Plugin]:
        """
        List all registered plugins.

        Returns:
            List of all Plugin instances (both enabled and disabled)
        """
        return list(self._plugins)

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """
        Get a specific plugin by name.

        Args:
            name: Plugin name to look up

        Returns:
            Plugin instance if found, None otherwise
        """
        for plugin in self._plugins:
            if plugin.name == name:
                return plugin
        return None

    def get_enabled_plugins(self) -> List[Plugin]:
        """
        Get only enabled plugins.

        Returns:
            List of enabled Plugin instances
        """
        return [p for p in self._plugins if p.enabled]

    def get_disabled_plugins(self) -> List[Plugin]:
        """
        Get only disabled plugins.

        Returns:
            List of disabled Plugin instances (typically due to load errors)
        """
        return [p for p in self._plugins if not p.enabled]

    def enable_plugin(self, name: str) -> bool:
        """
        Enable a disabled plugin.

        Args:
            name: Name of the plugin to enable

        Returns:
            True if plugin was found and enabled, False otherwise
        """
        plugin = self.get_plugin(name)
        if plugin is None:
            return False
        plugin.enabled = True
        return True

    def disable_plugin(self, name: str) -> bool:
        """
        Disable an enabled plugin.

        Args:
            name: Name of the plugin to disable

        Returns:
            True if plugin was found and disabled, False otherwise
        """
        plugin = self.get_plugin(name)
        if plugin is None:
            return False
        plugin.enabled = False
        return True

    def get_hooks_for_type(self, hook_name: str) -> List[str]:
        """
        Get names of all plugins that implement a specific hook.

        Args:
            hook_name: Hook type to query

        Returns:
            List of plugin names that implement the hook
        """
        return [
            p.name
            for p in self._plugins
            if p.enabled and p.has_hook(hook_name)
        ]

    def clear(self) -> None:
        """Remove all registered plugins and custom hooks."""
        self._plugins.clear()
        self._custom_hooks.clear()

    @property
    def plugin_count(self) -> int:
        """Total number of registered plugins."""
        return len(self._plugins)

    @property
    def enabled_count(self) -> int:
        """Number of enabled plugins."""
        return len(self.get_enabled_plugins())
