"""Извлечение полей из OCR текста."""

import logging
import re
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class FieldExtractor:
    """Извлечение структурированных полей из неструктурированного текста OCR."""

    def __init__(self):
        """Инициализация экстрактора полей."""
        # Паттерны для извлечения полей
        self.patterns = {
            "declaration_number": [
                r"номер\s+декларации[:\s]+([A-Z0-9\-]+)",
                r"declaration\s+number[:\s]+([A-Z0-9\-]+)",
                r"№\s*декларации[:\s]+([A-Z0-9\-]+)",
                r"ДТ[:\s]+([0-9\-]+)",
            ],
            "date_issued": [
                r"дата\s+выпуска[:\s]+(\d{1,2}[./]\d{1,2}[./]\d{2,4})",
                r"date\s+issued[:\s]+(\d{1,2}[./]\d{1,2}[./]\d{2,4})",
                r"(\d{4}-\d{2}-\d{2})",  # ISO формат
                r"(\d{1,2}\.\d{1,2}\.\d{4})",  # DD.MM.YYYY
            ],
            "manufacturer": [
                r"производитель[:\s]+([А-ЯЁA-Z][А-ЯЁа-яёA-Za-z\s\"']+)",
                r"manufacturer[:\s]+([A-Z][A-Za-z\s\"']+)",
                r"изготовитель[:\s]+([А-ЯЁA-Z][А-ЯЁа-яёA-Za-z\s\"']+)",
            ],
            "product_code": [
                r"код\s+товара[:\s]+(\d{10})",
                r"ТН\s*ВЭД[:\s]+(\d{10})",
                r"product\s+code[:\s]+(\d{10})",
                r"HS\s+code[:\s]+(\d{6,10})",
            ],
            "product_description": [
                r"описание\s+товара[:\s]+(.+?)(?=\n|код|стоимость|$)",
                r"product\s+description[:\s]+(.+?)(?=\n|code|value|$)",
                r"наименование\s+товара[:\s]+(.+?)(?=\n|код|стоимость|$)",
            ],
            "importer": [
                r"импортер[:\s]+([А-ЯЁA-Z][А-ЯЁа-яёA-Za-z\s\"']+)",
                r"importer[:\s]+([A-Z][A-Za-z\s\"']+)",
                r"получатель[:\s]+([А-ЯЁA-Z][А-ЯЁа-яёA-Za-z\s\"']+)",
            ],
            "country_origin": [
                r"страна\s+происхождения[:\s]+([A-Z]{2})",
                r"country\s+of\s+origin[:\s]+([A-Z]{2})",
                r"происхождение[:\s]+([А-ЯЁ]{2}|[A-Z]{2})",
            ],
            "customs_value": [
                r"таможенная\s+стоимость[:\s]+([\d\s,\.]+)",
                r"customs\s+value[:\s]+([\d\s,\.]+)",
                r"стоимость[:\s]+([\d\s,\.]+)",
            ],
            "currency": [
                r"валюта[:\s]+([A-Z]{3})",
                r"currency[:\s]+([A-Z]{3})",
                r"([A-Z]{3})\s+(?:USD|EUR|RUB|KZT)",
            ],
        }

    def extract_fields(self, text: str) -> dict[str, Any]:
        """Извлечение полей из текста OCR.

        Args:
            text: Неструктурированный текст из OCR.

        Returns:
            Словарь с извлеченными полями.
        """
        extracted: dict[str, Any] = {}

        for field_name, patterns in self.patterns.items():
            value = self._extract_field(text, patterns)
            if value:
                extracted[field_name] = value

        return extracted

    def _extract_field(self, text: str, patterns: list[str]) -> str | None:
        """Извлечение значения поля по паттернам.

        Args:
            text: Текст для поиска.
            patterns: Список регулярных выражений.

        Returns:
            Извлеченное значение или None.
        """
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                value = match.group(1).strip()
                # Очистка значения
                value = self._clean_value(value)
                if value:
                    return value

        return None

    def _clean_value(self, value: str) -> str:
        """Очистка извлеченного значения.

        Args:
            value: Исходное значение.

        Returns:
            Очищенное значение.
        """
        # Удаление лишних пробелов
        value = re.sub(r"\s+", " ", value.strip())

        # Удаление кавычек в начале и конце
        value = value.strip('"\'«»')

        return value

    def extract_declaration_number(self, text: str) -> str | None:
        """Извлечение номера декларации.

        Args:
            text: Текст для поиска.

        Returns:
            Номер декларации или None.
        """
        return self._extract_field(text, self.patterns["declaration_number"])

    def extract_date(self, text: str) -> datetime | None:
        """Извлечение даты.

        Args:
            text: Текст для поиска.

        Returns:
            Объект datetime или None.
        """
        date_str = self._extract_field(text, self.patterns["date_issued"])
        if not date_str:
            return None

        # Попытка парсинга различных форматов дат
        formats = [
            "%Y-%m-%d",
            "%d.%m.%Y",
            "%d/%m/%Y",
            "%d-%m-%Y",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        logger.warning(f"Не удалось распарсить дату: {date_str}")
        return None

    def extract_manufacturer(self, text: str) -> str | None:
        """Извлечение производителя.

        Args:
            text: Текст для поиска.

        Returns:
            Название производителя или None.
        """
        return self._extract_field(text, self.patterns["manufacturer"])

    def extract_product_code(self, text: str) -> str | None:
        """Извлечение кода товара.

        Args:
            text: Текст для поиска.

        Returns:
            Код товара или None.
        """
        code = self._extract_field(text, self.patterns["product_code"])
        if code:
            # Нормализация кода (только цифры)
            code = re.sub(r"[^\d]", "", code)
            # Дополнение до 10 цифр, если нужно
            if len(code) < 10:
                code = code.ljust(10, "0")
            elif len(code) > 10:
                code = code[:10]
        return code

    def extract_full_text_sections(self, text: str) -> dict[str, str]:
        """Извлечение секций из текста.

        Args:
            text: Текст для анализа.

        Returns:
            Словарь секций текста.
        """
        sections: dict[str, str] = {}

        # Разделение на строки
        lines = text.split("\n")

        current_section: str | None = None
        current_content: list[str] = []

        section_keywords = {
            "header": ["заголовок", "header", "шапка"],
            "goods": ["товары", "goods", "продукция"],
            "manufacturer": ["производитель", "manufacturer"],
            "customs_value": ["таможенная стоимость", "customs value"],
        }

        for line in lines:
            line_lower = line.lower().strip()

            # Проверка на начало новой секции
            detected_section = None
            for section_name, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    detected_section = section_name
                    break

            if detected_section:
                # Сохраняем предыдущую секцию
                if current_section and current_content:
                    sections[current_section] = "\n".join(current_content)

                # Начинаем новую секцию
                current_section = detected_section
                current_content = [line]
            else:
                # Продолжаем текущую секцию
                if current_section:
                    current_content.append(line)
                else:
                    # Общая секция
                    current_section = "general"
                    current_content.append(line)

        # Сохраняем последнюю секцию
        if current_section and current_content:
            sections[current_section] = "\n".join(current_content)

        return sections
