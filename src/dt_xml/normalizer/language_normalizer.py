"""Нормализация языков и текста."""

import logging
from typing import Any

try:
    from langdetect import detect, LangDetectException
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning("langdetect не установлен, используется базовая детекция языка")
    detect = None
    LangDetectException = Exception

logger = logging.getLogger(__name__)


class LanguageNormalizer:
    """Нормализация языков и текста."""

    def __init__(self):
        """Инициализация нормализатора языков."""
        self.supported_languages = {"ru", "kz", "en", "be", "hy", "ky"}

    def detect_language(self, text: str | None) -> str:
        """Определение языка текста.

        Args:
            text: Текст для определения языка.

        Returns:
            Код языка (ru, kz, en и т.д.).
        """
        if not text or not text.strip():
            return "ru"  # По умолчанию русский

        # Использование langdetect, если доступен
        if detect is not None:
            try:
                detected = detect(text)
                # Маппинг на поддерживаемые языки
                lang_map = {
                    "ru": "ru",
                    "kk": "kz",  # Казахский
                    "en": "en",
                    "be": "be",  # Белорусский
                    "hy": "hy",  # Армянский
                    "ky": "ky",  # Киргизский
                }
                return lang_map.get(detected, "ru")
            except LangDetectException:
                logger.warning(f"Не удалось определить язык для текста: {text[:100]}")

        # Fallback: простая эвристика
        return self._detect_language_heuristic(text)

    def _detect_language_heuristic(self, text: str) -> str:
        """Эвристическое определение языка.

        Args:
            text: Текст для определения.

        Returns:
            Код языка.
        """
        text_lower = text.lower()

        # Казахский язык - специфические буквы
        kazakh_chars = "әіңғұүқөһ"
        if any(char in text_lower for char in kazakh_chars):
            return "kz"

        # Киргизский язык
        kyrgyz_chars = "өү"
        if any(char in text_lower for char in kyrgyz_chars):
            return "ky"

        # Армянский язык
        if any("\u0530" <= char <= "\u058F" for char in text):
            return "hy"

        # Белорусский язык
        belarusian_chars = "іў"
        if any(char in text_lower for char in belarusian_chars):
            return "be"

        # Английский язык - проверка на латиницу
        if len(text) > 0 and all(ord(char) < 128 for char in text[:100]):
            return "en"

        # По умолчанию русский
        return "ru"

    def normalize_text_for_search(self, text: str | None, language: str | None = None) -> str | None:
        """Нормализация текста для поиска.

        Args:
            text: Текст для нормализации.
            language: Язык текста (если известен).

        Returns:
            Нормализованный текст или None.
        """
        if not text:
            return None

        # Определение языка, если не указан
        if not language:
            language = self.detect_language(text)

        # Базовая нормализация
        normalized = text.strip()

        # Удаление лишних пробелов
        normalized = " ".join(normalized.split())

        # Приведение к нижнему регистру для поиска
        normalized = normalized.lower()

        return normalized

    def get_language_info(self, text: str | None) -> dict[str, Any]:
        """Получение информации о языке текста.

        Args:
            text: Текст для анализа.

        Returns:
            Словарь с информацией о языке.
        """
        if not text:
            return {"language": "ru", "confidence": 0.0, "detected": False}

        detected_lang = self.detect_language(text)
        return {
            "language": detected_lang,
            "confidence": 1.0,  # В реальной реализации можно добавить оценку уверенности
            "detected": True,
        }
