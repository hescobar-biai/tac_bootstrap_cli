"""
IDK: plugin-contract, plugin-interface, hook-definition, plugin-metadata
Responsibility: Defines the plugin interface/contract and hook types for third-party extensibility
Invariants: Plugins must have name/version/author, hooks map to valid hook names,
            plugin state is immutable after initialization
"""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

# ============================================================================
# HOOK TYPES - Supported Extension Points
# ============================================================================


class HookType(str, Enum):
    """
    Supported hook types for plugin extensibility.

    Each hook type represents a specific extension point in the TAC Bootstrap
    lifecycle where plugins can inject custom behavior.
    """

    POST_PROJECT_CREATE = "post_project_create"
    PRE_SCAFFOLD = "pre_scaffold"
    POST_SCAFFOLD = "post_scaffold"
    ON_COMMAND = "on_command"
    ON_ERROR = "on_error"


# ============================================================================
# PLUGIN MODELS
# ============================================================================


class PluginManifest(BaseModel):
    """
    Plugin manifest metadata loaded from plugin.yaml.

    Describes the plugin's identity, version, capabilities, and configuration.

    Attributes:
        name: Unique plugin name (lowercase-hyphen format)
        version: Semantic version string (e.g., "1.0.0")
        author: Plugin author name or organization
        description: Short description of what the plugin does
        hooks: List of hook types this plugin implements
        dependencies: List of other plugin names this plugin depends on
        config: Optional plugin-specific configuration dictionary
    """

    name: str = Field(..., description="Unique plugin name (lowercase-hyphen format)")
    version: str = Field(..., description="Semantic version string (e.g., '1.0.0')")
    author: str = Field(..., description="Plugin author name or organization")
    description: str = Field(default="", description="Short description of the plugin")
    hooks: List[str] = Field(default_factory=list, description="List of hook types implemented")
    dependencies: List[str] = Field(
        default_factory=list, description="Other plugin names this plugin depends on"
    )
    config: Dict[str, Any] = Field(
        default_factory=dict, description="Plugin-specific configuration"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate plugin name is non-empty and uses lowercase-hyphen format."""
        if not v or not v.strip():
            raise ValueError("Plugin name cannot be empty")
        import re

        if not re.match(r"^[a-z][a-z0-9-]*$", v):
            raise ValueError(
                f"Plugin name '{v}' must be lowercase-hyphen format "
                "(lowercase letters, numbers, hyphens, must start with letter)"
            )
        return v.strip()

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        """Validate version follows semver-like format."""
        if not v or not v.strip():
            raise ValueError("Plugin version cannot be empty")
        import re

        if not re.match(r"^\d+\.\d+(\.\d+)?(-[a-zA-Z0-9.]+)?$", v):
            raise ValueError(
                f"Plugin version '{v}' must follow semantic versioning (e.g., '1.0.0')"
            )
        return v.strip()

    @field_validator("hooks")
    @classmethod
    def validate_hooks(cls, v: List[str]) -> List[str]:
        """Validate that all hook names are valid HookType values."""
        valid_hooks = {h.value for h in HookType}
        for hook_name in v:
            if hook_name not in valid_hooks:
                raise ValueError(
                    f"Invalid hook '{hook_name}'. Valid hooks: {', '.join(sorted(valid_hooks))}"
                )
        return v


class PluginHookResult(BaseModel):
    """
    Result of a plugin hook execution.

    Attributes:
        plugin_name: Name of the plugin that produced this result
        hook_name: Name of the hook that was executed
        success: Whether the hook execution succeeded
        message: Optional message from the hook execution
        data: Optional data returned by the hook
    """

    plugin_name: str = Field(..., description="Plugin that produced this result")
    hook_name: str = Field(..., description="Hook that was executed")
    success: bool = Field(default=True, description="Whether execution succeeded")
    message: str = Field(default="", description="Optional message from execution")
    data: Dict[str, Any] = Field(default_factory=dict, description="Optional data returned")


class Plugin:
    """
    Runtime representation of a loaded plugin.

    Combines manifest metadata with callable hook implementations discovered
    during plugin loading.

    Attributes:
        manifest: Plugin manifest metadata from plugin.yaml
        hooks: Dictionary mapping hook names to callable implementations
        enabled: Whether the plugin is currently active
        load_error: Error message if plugin failed to load
    """

    def __init__(
        self,
        manifest: PluginManifest,
        hooks: Optional[Dict[str, Callable[..., Any]]] = None,
        enabled: bool = True,
        load_error: Optional[str] = None,
    ) -> None:
        """
        Initialize a Plugin instance.

        Args:
            manifest: Plugin manifest metadata
            hooks: Dictionary of hook name to callable
            enabled: Whether plugin is active
            load_error: Error message if loading failed
        """
        self.manifest = manifest
        self.hooks: Dict[str, Callable[..., Any]] = hooks or {}
        self.enabled = enabled
        self.load_error = load_error

    @property
    def name(self) -> str:
        """Plugin name from manifest."""
        return self.manifest.name

    @property
    def version(self) -> str:
        """Plugin version from manifest."""
        return self.manifest.version

    @property
    def author(self) -> str:
        """Plugin author from manifest."""
        return self.manifest.author

    @property
    def description(self) -> str:
        """Plugin description from manifest."""
        return self.manifest.description

    def has_hook(self, hook_name: str) -> bool:
        """
        Check if this plugin implements a specific hook.

        Args:
            hook_name: Name of the hook to check

        Returns:
            True if the plugin has a callable for this hook
        """
        return hook_name in self.hooks and callable(self.hooks[hook_name])

    def execute_hook(self, hook_name: str, *args: Any, **kwargs: Any) -> PluginHookResult:
        """
        Execute a specific hook on this plugin.

        Args:
            hook_name: Name of the hook to execute
            *args: Positional arguments to pass to the hook
            **kwargs: Keyword arguments to pass to the hook

        Returns:
            PluginHookResult with execution outcome
        """
        if not self.enabled:
            return PluginHookResult(
                plugin_name=self.name,
                hook_name=hook_name,
                success=False,
                message="Plugin is disabled",
            )

        if not self.has_hook(hook_name):
            return PluginHookResult(
                plugin_name=self.name,
                hook_name=hook_name,
                success=False,
                message=f"Hook '{hook_name}' not implemented by plugin '{self.name}'",
            )

        try:
            result = self.hooks[hook_name](*args, **kwargs)
            data = result if isinstance(result, dict) else {}
            return PluginHookResult(
                plugin_name=self.name,
                hook_name=hook_name,
                success=True,
                message="Hook executed successfully",
                data=data,
            )
        except Exception as e:
            return PluginHookResult(
                plugin_name=self.name,
                hook_name=hook_name,
                success=False,
                message=f"Hook execution failed: {str(e)}",
            )

    def __repr__(self) -> str:
        """String representation of the plugin."""
        status = "enabled" if self.enabled else "disabled"
        return f"Plugin(name='{self.name}', version='{self.version}', status='{status}')"
