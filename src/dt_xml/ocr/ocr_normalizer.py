"""Нормализация данных из OCR."""

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


class OCRNormalizer:
    """Нормализация данных, извлеченных из OCR."""

    def __init__(self):
        """Инициализация нормализатора OCR."""
        pass

    def normalize(self, extracted_data: dict[str, Any]) -> dict[str, Any]:
        """Нормализация извлеченных данных.

        Args:
            extracted_data: Данные, извлеченные из OCR.

        Returns:
            Нормализованные данные.
        """
        normalized = extracted_data.copy()

        # Нормализация номеров деклараций
        if "declaration_number" in normalized:
            normalized["declaration_number"] = self._normalize_declaration_number(
                normalized["declaration_number"]
            )

        # Нормализация названий компаний
        if "manufacturer" in normalized:
            normalized["manufacturer"] = self._normalize_company_name(normalized["manufacturer"])

        if "importer" in normalized:
            normalized["importer"] = self._normalize_company_name(normalized["importer"])

        # Нормализация кодов товаров
        if "product_code" in normalized:
            normalized["product_code"] = self._normalize_product_code(normalized["product_code"])

        # Нормализация валют
        if "currency" in normalized:
            normalized["currency"] = self._normalize_currency(normalized["currency"])

        # Нормализация стран
        if "country_origin" in normalized:
            normalized["country_origin"] = self._normalize_country_code(normalized["country_origin"])

        # Нормализация числовых значений
        if "customs_value" in normalized:
            normalized["customs_value"] = self._normalize_number(normalized["customs_value"])

        return normalized

    def _normalize_declaration_number(self, value: str) -> str:
        """Нормализация номера декларации.

        Args:
            value: Номер декларации.

        Returns:
            Нормализованный номер.
        """
        # Удаление лишних символов, оставляем только буквы, цифры и дефисы
        normalized = re.sub(r"[^\w\-]", "", value.upper())
        return normalized

    def _normalize_company_name(self, value: str) -> str:
        """Нормализация названия компании.

        Args:
            value: Название компании.

        Returns:
            Нормализованное название.
        """
        # Удаление лишних пробелов
        normalized = re.sub(r"\s+", " ", value.strip())

        # Приведение к правильному регистру (первая буква заглавная)
        normalized = normalized.title()

        return normalized

    def _normalize_product_code(self, value: str) -> str:
        """Нормализация кода товара.

        Args:
            value: Код товара.

        Returns:
            Нормализованный код (10 цифр).
        """
        # Извлечение только цифр
        digits = re.sub(r"[^\d]", "", value)

        # Дополнение до 10 цифр или обрезка
        if len(digits) < 10:
            digits = digits.ljust(10, "0")
        elif len(digits) > 10:
            digits = digits[:10]

        return digits

    def _normalize_currency(self, value: str) -> str:
        """Нормализация кода валюты.

        Args:
            value: Код валюты.

        Returns:
            ISO код валюты.
        """
        value_upper = value.strip().upper()

        # Маппинг распространенных вариантов
        currency_map = {
            "RUB": "RUB",
            "RUR": "RUB",
            "РУБ": "RUB",
            "USD": "USD",
            "US$": "USD",
            "$": "USD",
            "EUR": "EUR",
            "€": "EUR",
            "ЕВРО": "EUR",
        }

        return currency_map.get(value_upper, value_upper)

    def _normalize_country_code(self, value: str) -> str:
        """Нормализация кода страны.

        Args:
            value: Код или название страны.

        Returns:
            ISO код страны.
        """
        value_upper = value.strip().upper()

        # Маппинг названий стран на ISO коды
        country_map = {
            "RU": "RU",
            "RUS": "RU",
            "РОССИЯ": "RU",
            "РФ": "RU",
            "CN": "CN",
            "CHN": "CN",
            "КИТАЙ": "CN",
            "US": "US",
            "USA": "US",
            "США": "US",
        }

        return country_map.get(value_upper, value_upper)

    def _normalize_number(self, value: str) -> float | None:
        """Нормализация числового значения.

        Args:
            value: Числовое значение в виде строки.

        Returns:
            Число или None.
        """
        try:
            # Удаление пробелов и замена запятой на точку
            cleaned = value.replace(" ", "").replace(",", ".")
            return float(cleaned)
        except (ValueError, AttributeError):
            logger.warning(f"Не удалось нормализовать число: {value}")
            return None
