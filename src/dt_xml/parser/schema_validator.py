"""Валидатор схемы XML деклараций ЕАЭС."""

import logging
from pathlib import Path
from typing import Any

from lxml import etree

logger = logging.getLogger(__name__)


class SchemaValidator:
    """Валидатор XML схемы деклараций ЕАЭС."""

    def __init__(self, schema_path: Path | None = None):
        """Инициализация валидатора.

        Args:
            schema_path: Путь к XSD схеме. Если None, используется базовая валидация структуры.
        """
        self.schema_path = schema_path
        self.schema: etree.XMLSchema | None = None
        if schema_path and schema_path.exists():
            try:
                schema_doc = etree.parse(str(schema_path))
                self.schema = etree.XMLSchema(schema_doc)
                logger.info(f"Загружена XSD схема из {schema_path}")
            except Exception as e:
                logger.warning(f"Не удалось загрузить XSD схему: {e}. Используется базовая валидация.")

    def validate(self, xml_content: str | bytes) -> tuple[bool, list[str]]:
        """Валидация XML контента.

        Args:
            xml_content: XML контент для валидации.

        Returns:
            Кортеж (валиден ли документ, список ошибок).
        """
        errors: list[str] = []

        try:
            if isinstance(xml_content, str):
                xml_content = xml_content.encode("utf-8")

            doc = etree.fromstring(xml_content)

            # Валидация по XSD схеме, если она загружена
            if self.schema is not None:
                try:
                    self.schema.assertValid(doc)
                except etree.DocumentInvalid as e:
                    errors.append(f"XSD валидация не пройдена: {e}")
                    return False, errors

            # Базовая валидация структуры
            structure_errors = self._validate_structure(doc)
            errors.extend(structure_errors)

            return len(errors) == 0, errors

        except etree.XMLSyntaxError as e:
            errors.append(f"XML синтаксическая ошибка: {e}")
            return False, errors
        except Exception as e:
            errors.append(f"Ошибка при валидации: {e}")
            return False, errors

    def _validate_structure(self, doc: etree._Element) -> list[str]:
        """Базовая валидация структуры документа.

        Args:
            doc: Корневой элемент XML документа.

        Returns:
            Список ошибок валидации.
        """
        errors: list[str] = []

        # Проверка наличия корневого элемента
        if doc.tag is None:
            errors.append("Отсутствует корневой элемент")

        # Проверка наличия основных полей (базовая проверка)
        # В реальной реализации здесь должна быть проверка по схеме ЕАЭС
        required_paths = [
            ".//declaration_number",
            ".//date_issued",
        ]

        for path in required_paths:
            elements = doc.xpath(path)
            if not elements:
                errors.append(f"Отсутствует обязательное поле: {path}")

        return errors

    def get_schema_info(self) -> dict[str, Any]:
        """Получить информацию о схеме.

        Returns:
            Словарь с информацией о схеме.
        """
        return {
            "schema_loaded": self.schema is not None,
            "schema_path": str(self.schema_path) if self.schema_path else None,
        }
