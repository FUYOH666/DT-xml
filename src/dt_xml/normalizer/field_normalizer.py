"""Нормализация полей деклараций."""

import logging
import re
from typing import Any

from unidecode import unidecode

logger = logging.getLogger(__name__)


class FieldNormalizer:
    """Нормализация полей деклараций."""

    def __init__(self):
        """Инициализация нормализатора."""
        # Паттерны для очистки текста
        self.whitespace_pattern = re.compile(r"\s+")
        self.special_chars_pattern = re.compile(r"[^\w\s\-.,()]")

    def normalize_company_name(self, name: str | None) -> str | None:
        """Нормализация названия компании.

        Args:
            name: Название компании.

        Returns:
            Нормализованное название или None.
        """
        if not name:
            return None

        # Удаление лишних пробелов
        normalized = self.whitespace_pattern.sub(" ", name.strip())

        # Приведение к единому регистру (сохраняем первую букву заглавной)
        normalized = normalized.title()

        # Удаление общих префиксов/суффиксов для унификации
        prefixes = ["ООО", "ОАО", "ЗАО", "ПАО", "ИП", "LLC", "LTD", "INC"]
        for prefix in prefixes:
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix) :].strip()

        return normalized

    def normalize_manufacturer(self, manufacturer: str | None) -> str | None:
        """Нормализация названия производителя.

        Args:
            manufacturer: Название производителя.

        Returns:
            Нормализованное название или None.
        """
        return self.normalize_company_name(manufacturer)

    def normalize_text(self, text: str | None) -> str | None:
        """Нормализация текстового поля.

        Args:
            text: Текст для нормализации.

        Returns:
            Нормализованный текст или None.
        """
        if not text:
            return None

        # Удаление лишних пробелов
        normalized = self.whitespace_pattern.sub(" ", text.strip())

        # Удаление специальных символов (опционально, можно настроить)
        # normalized = self.special_chars_pattern.sub("", normalized)

        return normalized

    def normalize_currency(self, currency: str | None) -> str | None:
        """Нормализация кода валюты.

        Args:
            currency: Код валюты.

        Returns:
            Нормализованный код валюты (ISO 4217) или None.
        """
        if not currency:
            return None

        currency_upper = currency.strip().upper()

        # Маппинг распространенных вариантов на ISO коды
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
            "KZT": "KZT",
            "ТЕНГЕ": "KZT",
            "BYN": "BYN",
            "БЕЛ.РУБ": "BYN",
        }

        return currency_map.get(currency_upper, currency_upper)

    def normalize_country_code(self, country: str | None) -> str | None:
        """Нормализация кода страны.

        Args:
            country: Код или название страны.

        Returns:
            ISO код страны или None.
        """
        if not country:
            return None

        country_upper = country.strip().upper()

        # Маппинг названий стран на ISO коды
        country_map = {
            "RU": "RU",
            "RUS": "RU",
            "РОССИЯ": "RU",
            "РФ": "RU",
            "KZ": "KZ",
            "KAZ": "KZ",
            "КАЗАХСТАН": "KZ",
            "BY": "BY",
            "BLR": "BY",
            "БЕЛАРУСЬ": "BY",
            "AM": "AM",
            "ARM": "AM",
            "АРМЕНИЯ": "AM",
            "KG": "KG",
            "KGZ": "KG",
            "КЫРГЫЗСТАН": "KG",
            "CN": "CN",
            "CHN": "CN",
            "КИТАЙ": "CN",
            "US": "US",
            "USA": "US",
            "США": "US",
            "DE": "DE",
            "DEU": "DE",
            "ГЕРМАНИЯ": "DE",
        }

        return country_map.get(country_upper, country_upper)

    def normalize_decimal(self, value: str | float | None) -> float | None:
        """Нормализация десятичного числа.

        Args:
            value: Значение для нормализации.

        Returns:
            Нормализованное число или None.
        """
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            # Замена запятой на точку, удаление пробелов
            cleaned = value.strip().replace(",", ".").replace(" ", "")
            try:
                return float(cleaned)
            except ValueError:
                logger.warning(f"Не удалось преобразовать в число: {value}")
                return None

        return None

    def normalize_phone(self, phone: str | None) -> str | None:
        """Нормализация номера телефона.

        Args:
            phone: Номер телефона.

        Returns:
            Нормализованный номер или None.
        """
        if not phone:
            return None

        # Удаление всех нецифровых символов кроме +
        normalized = re.sub(r"[^\d+]", "", phone.strip())

        return normalized

    def normalize_email(self, email: str | None) -> str | None:
        """Нормализация email адреса.

        Args:
            email: Email адрес.

        Returns:
            Нормализованный email или None.
        """
        if not email:
            return None

        normalized = email.strip().lower()

        # Базовая валидация формата
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        if not email_pattern.match(normalized):
            logger.warning(f"Некорректный формат email: {email}")
            return None

        return normalized

    def normalize_all_fields(self, data: dict[str, Any]) -> dict[str, Any]:
        """Нормализация всех полей в словаре данных.

        Args:
            data: Словарь с данными декларации.

        Returns:
            Словарь с нормализованными данными.
        """
        normalized = data.copy()

        # Нормализация компаний
        if "manufacturer" in normalized:
            normalized["manufacturer"] = self.normalize_manufacturer(normalized["manufacturer"])
        if "importer" in normalized:
            normalized["importer"] = self.normalize_company_name(normalized["importer"])
        if "exporter" in normalized:
            normalized["exporter"] = self.normalize_company_name(normalized["exporter"])

        # Нормализация текстовых полей
        if "product_description" in normalized:
            normalized["product_description"] = self.normalize_text(normalized["product_description"])
        if "full_text" in normalized:
            normalized["full_text"] = self.normalize_text(normalized["full_text"])

        # Нормализация кодов
        if "currency" in normalized:
            normalized["currency"] = self.normalize_currency(normalized["currency"])
        if "country_origin" in normalized:
            normalized["country_origin"] = self.normalize_country_code(normalized["country_origin"])

        # Нормализация чисел
        if "customs_value" in normalized:
            normalized["customs_value"] = self.normalize_decimal(normalized["customs_value"])
        if "quantity" in normalized:
            normalized["quantity"] = self.normalize_decimal(normalized["quantity"])

        return normalized
