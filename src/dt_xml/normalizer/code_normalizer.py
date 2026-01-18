"""Нормализация кодов (ТН ВЭД, ISO и т.д.)."""

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


class CodeNormalizer:
    """Нормализация кодов товаров и других кодов."""

    def __init__(self):
        """Инициализация нормализатора кодов."""
        # Паттерн для кода ТН ВЭД (10 цифр)
        self.tn_ved_pattern = re.compile(r"(\d{10})")

    def normalize_tn_ved_code(self, code: str | None) -> str | None:
        """Нормализация кода ТН ВЭД.

        Args:
            code: Код ТН ВЭД.

        Returns:
            Нормализованный код (10 цифр) или None.
        """
        if not code:
            return None

        # Извлечение только цифр
        digits_only = re.sub(r"[^\d]", "", str(code))

        # Код ТН ВЭД должен быть 10 цифр
        if len(digits_only) == 10:
            return digits_only
        elif len(digits_only) > 10:
            # Берем первые 10 цифр
            logger.warning(f"Код ТН ВЭД длиннее 10 цифр: {code}, обрезано до {digits_only[:10]}")
            return digits_only[:10]
        elif len(digits_only) >= 4:
            # Дополняем нулями справа до 10 цифр
            normalized = digits_only.ljust(10, "0")
            logger.info(f"Код ТН ВЭД дополнен нулями: {code} -> {normalized}")
            return normalized
        else:
            logger.warning(f"Некорректный код ТН ВЭД: {code}")
            return None

    def normalize_hs_code(self, code: str | None) -> str | None:
        """Нормализация кода HS (Harmonized System).

        Args:
            code: Код HS.

        Returns:
            Нормализованный код или None.
        """
        # HS код может быть 6, 8 или 10 цифр
        if not code:
            return None

        digits_only = re.sub(r"[^\d]", "", str(code))

        if len(digits_only) >= 6:
            return digits_only[:10]  # Максимум 10 цифр
        else:
            logger.warning(f"Некорректный код HS: {code}")
            return None

    def normalize_product_code(self, code: str | None) -> str | None:
        """Нормализация кода товара (универсальный метод).

        Args:
            code: Код товара.

        Returns:
            Нормализованный код или None.
        """
        if not code:
            return None

        # Пробуем ТН ВЭД формат
        normalized = self.normalize_tn_ved_code(code)
        if normalized:
            return normalized

        # Пробуем HS формат
        normalized = self.normalize_hs_code(code)
        if normalized:
            return normalized

        # Возвращаем как есть, если не удалось нормализовать
        return str(code).strip()

    def extract_tn_ved_from_text(self, text: str | None) -> list[str]:
        """Извлечение кодов ТН ВЭД из текста.

        Args:
            text: Текст для поиска кодов.

        Returns:
            Список найденных кодов ТН ВЭД.
        """
        if not text:
            return []

        codes = self.tn_ved_pattern.findall(text)
        normalized_codes = []

        for code in codes:
            normalized = self.normalize_tn_ved_code(code)
            if normalized and normalized not in normalized_codes:
                normalized_codes.append(normalized)

        return normalized_codes

    def validate_tn_ved_code(self, code: str | None) -> bool:
        """Валидация кода ТН ВЭД.

        Args:
            code: Код для валидации.

        Returns:
            True если код валиден, False иначе.
        """
        if not code:
            return False

        normalized = self.normalize_tn_ved_code(code)
        return normalized is not None and len(normalized) == 10

    def get_code_hierarchy(self, code: str | None) -> dict[str, str] | None:
        """Получение иерархии кода ТН ВЭД.

        Args:
            code: Код ТН ВЭД.

        Returns:
            Словарь с уровнями иерархии или None.
        """
        normalized = self.normalize_tn_ved_code(code)
        if not normalized or len(normalized) != 10:
            return None

        return {
            "full": normalized,  # 10 цифр
            "group": normalized[:8],  # 8 цифр
            "subgroup": normalized[:6],  # 6 цифр
            "chapter": normalized[:4],  # 4 цифры
            "section": normalized[:2],  # 2 цифры
        }
