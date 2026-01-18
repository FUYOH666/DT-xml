"""Валидация данных по динамической схеме."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class SchemaValidator:
    """Валидатор данных по динамической схеме."""

    def __init__(self, schema_config: dict[str, Any] | None = None):
        """Инициализация валидатора.

        Args:
            schema_config: Конфигурация схемы заказчика.
        """
        self.schema_config = schema_config or {}
        self.required_fields = self._extract_required_fields()

    def _extract_required_fields(self) -> list[str]:
        """Извлечение обязательных полей из схемы.

        Returns:
            Список обязательных полей.
        """
        schema = self.schema_config.get("schema", {})
        required_for_search = schema.get("required_for_search", [])

        # Базовые обязательные поля (P0)
        base_required = ["declaration_number", "date_issued", "declaration_type"]

        # Объединение базовых и специфичных для поиска
        all_required = list(set(base_required + required_for_search))

        return all_required

    def validate(self, data: dict[str, Any]) -> tuple[bool, list[str]]:
        """Валидация данных по схеме.

        Args:
            data: Данные для валидации.

        Returns:
            Кортеж (валидны ли данные, список ошибок).
        """
        errors: list[str] = []
        missing_fields: list[str] = []

        # Проверка обязательных полей
        for field in self.required_fields:
            if field not in data or data[field] is None or data[field] == "":
                missing_fields.append(field)

        if missing_fields:
            errors.append(f"Отсутствуют обязательные поля: {', '.join(missing_fields)}")

        # Проверка типов полей (если указаны в схеме)
        schema = self.schema_config.get("schema", {})
        field_types = schema.get("field_types", {})

        for field, expected_type in field_types.items():
            if field in data:
                if not self._validate_field_type(data[field], expected_type):
                    errors.append(f"Поле '{field}' имеет неверный тип. Ожидается: {expected_type}")

        return len(errors) == 0, errors

    def _validate_field_type(self, value: Any, expected_type: str) -> bool:
        """Валидация типа поля.

        Args:
            value: Значение поля.
            expected_type: Ожидаемый тип.

        Returns:
            True если тип соответствует.
        """
        type_map = {
            "string": str,
            "integer": int,
            "float": float,
            "number": (int, float),
            "boolean": bool,
            "date": str,  # Даты хранятся как строки
        }

        python_type = type_map.get(expected_type.lower())
        if python_type is None:
            return True  # Неизвестный тип - пропускаем

        return isinstance(value, python_type)

    def get_required_fields(self) -> list[str]:
        """Получение списка обязательных полей.

        Returns:
            Список обязательных полей.
        """
        return self.required_fields.copy()

    def get_field_priority(self, field: str) -> str:
        """Получение приоритета поля.

        Args:
            field: Имя поля.

        Returns:
            Приоритет поля (P0, P1, P2).
        """
        # P0 - базовые обязательные поля
        p0_fields = ["declaration_number", "date_issued", "declaration_type"]
        if field in p0_fields:
            return "P0"

        # P1 - критичные для поиска
        schema = self.schema_config.get("schema", {})
        required_for_search = schema.get("required_for_search", [])
        if field in required_for_search:
            return "P1"

        # P2 - остальные поля
        return "P2"
