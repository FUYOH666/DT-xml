"""Маппинг полей между схемами."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class FieldMapper:
    """Маппинг полей из входного формата в внутренний."""

    def __init__(self, field_mapping: dict[str, list[str]] | None = None):
        """Инициализация маппера полей.

        Args:
            field_mapping: Словарь маппинга (целевое_поле -> список_возможных_имен).
        """
        self.field_mapping = field_mapping or {}

    def map_fields(self, data: dict[str, Any]) -> dict[str, Any]:
        """Маппинг полей из входных данных.

        Args:
            data: Входные данные с полями.

        Returns:
            Данные с переименованными полями согласно схеме.
        """
        mapped_data: dict[str, Any] = {}

        for target_field, possible_names in self.field_mapping.items():
            # Поиск значения по возможным именам полей
            value = self._find_field_value(data, possible_names)
            if value is not None:
                mapped_data[target_field] = value

        # Копирование остальных полей, которые не в маппинге
        for key, value in data.items():
            if key not in mapped_data:
                mapped_data[key] = value

        return mapped_data

    def _find_field_value(self, data: dict[str, Any], possible_names: list[str]) -> Any:
        """Поиск значения поля по списку возможных имен.

        Args:
            data: Словарь данных.
            possible_names: Список возможных имен поля.

        Returns:
            Значение поля или None.
        """
        # Прямой поиск
        for name in possible_names:
            if name in data:
                return data[name]

        # Поиск без учета регистра
        data_lower = {k.lower(): v for k, v in data.items()}
        for name in possible_names:
            if name.lower() in data_lower:
                return data_lower[name.lower()]

        # Поиск вложенных структур
        for name in possible_names:
            value = self._get_nested_value(data, name)
            if value is not None:
                return value

        return None

    def _get_nested_value(self, data: dict[str, Any], key: str) -> Any:
        """Получение значения из вложенной структуры.

        Args:
            data: Словарь данных.
            key: Ключ (может быть вложенным через точку).

        Returns:
            Значение или None.
        """
        keys = key.split(".")
        current = data

        for k in keys:
            if isinstance(current, dict):
                current = current.get(k)
                if current is None:
                    return None
            else:
                return None

        return current

    def get_mapping_info(self) -> dict[str, list[str]]:
        """Получение информации о маппинге.

        Returns:
            Словарь маппинга полей.
        """
        return self.field_mapping.copy()
