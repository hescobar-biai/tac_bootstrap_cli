"""
IDK: i18n-service, internationalization, multi-language, translation, locale-management
Responsibility: Provides gettext-like i18n system with JSON translation files for CLI output
Invariants: Falls back to English when translation missing, thread-safe singleton pattern,
            supports 6 languages (en, es, fr, de, ja, zh)

Example usage:
    from tac_bootstrap.infrastructure.i18n import I18nService, t

    # Using the global translation function
    print(t("cli.welcome"))           # "Welcome to TAC Bootstrap"
    print(t("cli.version", v="1.0"))  # "TAC Bootstrap v1.0"

    # Using the service directly
    i18n = I18nService()
    i18n.set_language("es")
    print(i18n.translate("cli.welcome"))  # "Bienvenido a TAC Bootstrap"
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


# Supported languages with their display names
SUPPORTED_LANGUAGES: Dict[str, str] = {
    "en": "English",
    "es": "Espanol",
    "fr": "Francais",
    "de": "Deutsch",
    "ja": "Japanese",
    "zh": "Chinese (Simplified)",
}

# Default language
DEFAULT_LANGUAGE = "en"


class I18nService:
    """
    IDK: i18n-core, translation-engine, locale-loader, language-switching
    Responsibility: Loads JSON translation files and provides key-based translation lookup
    Invariants: Singleton instance, English fallback for missing keys, lazy-loads translations
    """

    _instance: Optional["I18nService"] = None
    _initialized: bool = False

    def __new__(cls) -> "I18nService":
        """Singleton pattern to ensure single translation state across the app."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the i18n service with default language."""
        if self._initialized:
            return
        self._current_language: str = DEFAULT_LANGUAGE
        self._translations: Dict[str, Dict[str, Any]] = {}
        self._locales_dir: Path = Path(__file__).parent.parent / "locales"
        self._config_file: Path = Path.home() / ".tac-bootstrap" / ".language_config"
        self._load_saved_language()
        self._initialized = True

    def _load_saved_language(self) -> None:
        """Load previously saved language preference from config file."""
        if self._config_file.exists():
            try:
                lang = self._config_file.read_text().strip()
                if lang in SUPPORTED_LANGUAGES:
                    self._current_language = lang
            except OSError:
                pass

    def _load_translations(self, language: str) -> Dict[str, Any]:
        """Load translations for a specific language from its JSON file.

        Args:
            language: Language code (e.g., 'en', 'es', 'fr')

        Returns:
            Dictionary of translation key-value pairs (possibly nested)
        """
        if language in self._translations:
            return self._translations[language]

        locale_file = self._locales_dir / f"{language}.json"
        if not locale_file.exists():
            self._translations[language] = {}
            return {}

        try:
            with open(locale_file, "r", encoding="utf-8") as f:
                translations = json.load(f)
            self._translations[language] = translations
            return translations
        except (json.JSONDecodeError, OSError):
            self._translations[language] = {}
            return {}

    def _resolve_key(self, translations: Dict[str, Any], key: str) -> Optional[str]:
        """Resolve a dot-separated key in nested translation dict.

        Args:
            translations: Translation dictionary (possibly nested)
            key: Dot-separated key like "cli.welcome" or "errors.not_found"

        Returns:
            The translation string, or None if key not found
        """
        parts = key.split(".")
        current: Any = translations
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        if isinstance(current, str):
            return current
        return None

    @property
    def current_language(self) -> str:
        """Get the current language code."""
        return self._current_language

    @property
    def current_language_name(self) -> str:
        """Get the display name for the current language."""
        return SUPPORTED_LANGUAGES.get(self._current_language, "Unknown")

    def set_language(self, language: str) -> bool:
        """Set the current language and persist the preference.

        Args:
            language: Language code (e.g., 'en', 'es', 'fr', 'de', 'ja', 'zh')

        Returns:
            True if language was set successfully, False if language is not supported
        """
        if language not in SUPPORTED_LANGUAGES:
            return False
        self._current_language = language
        # Persist the preference
        try:
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            self._config_file.write_text(language)
        except OSError:
            pass
        return True

    def translate(self, key: str, **kwargs: Any) -> str:
        """Translate a key with optional variable substitution.

        Looks up the key in the current language, falls back to English
        if not found, and returns the key itself as last resort.

        Args:
            key: Translation key (dot-separated, e.g., "cli.welcome")
            **kwargs: Variables for string formatting (e.g., name="World")

        Returns:
            Translated and formatted string
        """
        # Try current language
        translations = self._load_translations(self._current_language)
        result = self._resolve_key(translations, key)

        # Fallback to English
        if result is None and self._current_language != DEFAULT_LANGUAGE:
            en_translations = self._load_translations(DEFAULT_LANGUAGE)
            result = self._resolve_key(en_translations, key)

        # Last resort: return the key itself
        if result is None:
            return key

        # Apply variable substitution
        if kwargs:
            try:
                result = result.format(**kwargs)
            except (KeyError, IndexError):
                pass

        return result

    def get_supported_languages(self) -> Dict[str, str]:
        """Get dictionary of supported language codes and their display names.

        Returns:
            Dict mapping language codes to display names
        """
        return dict(SUPPORTED_LANGUAGES)

    def get_all_keys(self, language: Optional[str] = None) -> List[str]:
        """Get all translation keys for a language (for testing/validation).

        Args:
            language: Language code (defaults to current language)

        Returns:
            List of all dot-separated translation keys
        """
        lang = language or self._current_language
        translations = self._load_translations(lang)
        keys: List[str] = []
        self._collect_keys(translations, "", keys)
        return keys

    def _collect_keys(self, d: Dict[str, Any], prefix: str, keys: List[str]) -> None:
        """Recursively collect all dot-separated keys from nested dict."""
        for k, v in d.items():
            full_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                self._collect_keys(v, full_key, keys)
            else:
                keys.append(full_key)

    def has_key(self, key: str, language: Optional[str] = None) -> bool:
        """Check if a translation key exists for a given language.

        Args:
            key: Translation key
            language: Language code (defaults to current language)

        Returns:
            True if the key has a translation
        """
        lang = language or self._current_language
        translations = self._load_translations(lang)
        return self._resolve_key(translations, key) is not None

    def reset(self) -> None:
        """Reset i18n service to defaults (useful for testing)."""
        self._current_language = DEFAULT_LANGUAGE
        self._translations = {}

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        cls._instance = None
        cls._initialized = False


def t(key: str, **kwargs: Any) -> str:
    """Global translation shortcut function.

    Convenience function that uses the singleton I18nService instance.

    Args:
        key: Translation key (dot-separated)
        **kwargs: Variables for string formatting

    Returns:
        Translated string

    Example:
        print(t("cli.welcome"))
        print(t("cli.version", v="1.0.0"))
    """
    return I18nService().translate(key, **kwargs)
