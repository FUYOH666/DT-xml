"""Извлечение секций из деклараций."""

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


class SectionExtractor:
    """Извлечение логических секций из деклараций."""

    def __init__(self):
        """Инициализация экстрактора секций."""
        # Паттерны для определения секций декларации
        self.section_patterns = {
            "header": re.compile(r"(заголовок|header|шапка)", re.IGNORECASE),
            "declarant": re.compile(r"(декларант|declarant|заявитель)", re.IGNORECASE),
            "goods": re.compile(r"(товары|goods|продукция|товар)", re.IGNORECASE),
            "manufacturer": re.compile(r"(производитель|manufacturer|изготовитель)", re.IGNORECASE),
            "importer": re.compile(r"(импортер|importer|получатель)", re.IGNORECASE),
            "exporter": re.compile(r"(экспортер|exporter|отправитель)", re.IGNORECASE),
            "customs_value": re.compile(r"(таможенная\s+стоимость|customs\s+value|стоимость)", re.IGNORECASE),
            "payment": re.compile(r"(платежи|payment|оплата|таможенные\s+платежи)", re.IGNORECASE),
            "transport": re.compile(r"(транспорт|transport|доставка)", re.IGNORECASE),
            "documents": re.compile(r"(документы|documents|приложения)", re.IGNORECASE),
        }

    def extract_sections(self, text: str, data: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Извлечение секций из текста и данных.

        Args:
            text: Текст декларации.
            data: Структурированные данные декларации.

        Returns:
            Список секций с содержимым.
        """
        sections: list[dict[str, Any]] = []

        # Извлечение секций из структурированных данных
        if data:
            structured_sections = self._extract_from_structure(data)
            sections.extend(structured_sections)

        # Извлечение секций из текста
        text_sections = self._extract_from_text(text)
        sections.extend(text_sections)

        # Удаление дубликатов и объединение
        merged_sections = self._merge_sections(sections)

        return merged_sections

    def _extract_from_structure(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        """Извлечение секций из структурированных данных.

        Args:
            data: Словарь с данными декларации.

        Returns:
            Список секций.
        """
        sections: list[dict[str, Any]] = []

        # Секция заголовка
        if "declaration_number" in data or "date_issued" in data:
            header_content = []
            if "declaration_number" in data:
                header_content.append(f"Номер декларации: {data['declaration_number']}")
            if "date_issued" in data:
                header_content.append(f"Дата выпуска: {data['date_issued']}")
            if header_content:
                sections.append(
                    {
                        "section": "header",
                        "content": "\n".join(header_content),
                        "metadata": {"type": "structured"},
                    }
                )

        # Секция производителя
        if "manufacturer" in data and data["manufacturer"]:
            sections.append(
                {
                    "section": "manufacturer",
                    "content": f"Производитель: {data['manufacturer']}",
                    "metadata": {"manufacturer": data["manufacturer"]},
                }
            )

        # Секция импортера
        if "importer" in data and data["importer"]:
            sections.append(
                {
                    "section": "importer",
                    "content": f"Импортер: {data['importer']}",
                    "metadata": {"importer": data["importer"]},
                }
            )

        # Секция товаров
        goods_content = []
        if "product_code" in data and data["product_code"]:
            goods_content.append(f"Код товара (ТН ВЭД): {data['product_code']}")
        if "product_description" in data and data["product_description"]:
            goods_content.append(f"Описание: {data['product_description']}")
        if "country_origin" in data and data["country_origin"]:
            goods_content.append(f"Страна происхождения: {data['country_origin']}")
        if "quantity" in data and data["quantity"]:
            unit = data.get("unit_of_measure", "")
            goods_content.append(f"Количество: {data['quantity']} {unit}")
        if goods_content:
            sections.append(
                {
                    "section": "goods",
                    "content": "\n".join(goods_content),
                    "metadata": {
                        "product_code": data.get("product_code"),
                        "country_origin": data.get("country_origin"),
                    },
                }
            )

        # Секция таможенной стоимости
        if "customs_value" in data and data["customs_value"]:
            currency = data.get("currency", "")
            sections.append(
                {
                    "section": "customs_value",
                    "content": f"Таможенная стоимость: {data['customs_value']} {currency}",
                    "metadata": {
                        "customs_value": data["customs_value"],
                        "currency": currency,
                    },
                }
            )

        return sections

    def _extract_from_text(self, text: str) -> list[dict[str, Any]]:
        """Извлечение секций из текста.

        Args:
            text: Текст декларации.

        Returns:
            Список секций.
        """
        if not text:
            return []

        sections: list[dict[str, Any]] = []
        lines = text.split("\n")

        current_section: str | None = None
        current_content: list[str] = []

        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue

            # Проверка на начало новой секции
            detected_section = self._detect_section(line_stripped)
            if detected_section:
                # Сохраняем предыдущую секцию
                if current_section and current_content:
                    sections.append(
                        {
                            "section": current_section,
                            "content": "\n".join(current_content),
                            "metadata": {"type": "text"},
                        }
                    )
                # Начинаем новую секцию
                current_section = detected_section
                current_content = [line_stripped]
            else:
                # Продолжаем текущую секцию
                if current_section:
                    current_content.append(line_stripped)
                else:
                    # Если секция не определена, относим к общей секции
                    current_section = "general"
                    current_content = [line_stripped]

        # Сохраняем последнюю секцию
        if current_section and current_content:
            sections.append(
                {
                    "section": current_section,
                    "content": "\n".join(current_content),
                    "metadata": {"type": "text"},
                }
            )

        return sections

    def _detect_section(self, text: str) -> str | None:
        """Определение секции по тексту.

        Args:
            text: Текст для анализа.

        Returns:
            Название секции или None.
        """
        for section_name, pattern in self.section_patterns.items():
            if pattern.search(text):
                return section_name

        return None

    def _merge_sections(self, sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Объединение дублирующихся секций.

        Args:
            sections: Список секций.

        Returns:
            Объединенный список секций.
        """
        merged: dict[str, dict[str, Any]] = {}

        for section in sections:
            section_name = section["section"]
            if section_name in merged:
                # Объединяем содержимое
                existing_content = merged[section_name]["content"]
                new_content = section["content"]
                merged[section_name]["content"] = f"{existing_content}\n{new_content}"

                # Объединяем метаданные
                existing_metadata = merged[section_name].get("metadata", {})
                new_metadata = section.get("metadata", {})
                existing_metadata.update(new_metadata)
                merged[section_name]["metadata"] = existing_metadata
            else:
                merged[section_name] = section.copy()

        return list(merged.values())
