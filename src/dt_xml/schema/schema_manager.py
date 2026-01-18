"""Менеджер схем данных."""

import logging
from typing import Any

from dt_xml.schema.field_mapper import FieldMapper
from dt_xml.schema.schema_registry import SchemaRegistry
from dt_xml.schema.schema_validator import SchemaValidator

logger = logging.getLogger(__name__)


class SchemaManager:
    """Менеджер схем данных для заказчиков."""

    def __init__(self, config_path: str | None = None):
        """Инициализация менеджера схем.

        Args:
            config_path: Путь к директории с конфигурациями.
        """
        self.registry = SchemaRegistry(config_path)
        self.current_tenant: str | None = None
        self.current_schema: dict[str, Any] | None = None
        self.field_mapper: FieldMapper | None = None
        self.validator: SchemaValidator | None = None

    def load_tenant_schema(self, tenant_id: str) -> None:
        """Загрузка схемы для заказчика.

        Args:
            tenant_id: Идентификатор заказчика.
        """
        schema_config = self.registry.get_schema(tenant_id)

        if schema_config is None:
            logger.warning(f"Схема для заказчика {tenant_id} не найдена, используется default")
            schema_config = self.registry.get_schema("default")

        if schema_config is None:
            raise ValueError(f"Схема для заказчика {tenant_id} не найдена и default схема отсутствует")

        self.current_tenant = tenant_id
        self.current_schema = schema_config

        # Инициализация маппера полей
        field_mapping = schema_config.get("schema", {}).get("field_mapping", {})
        self.field_mapper = FieldMapper(field_mapping)

        # Инициализация валидатора
        self.validator = SchemaValidator(schema_config)

        logger.info(f"Загружена схема для заказчика: {tenant_id}")

    def map_fields(self, data: dict[str, Any]) -> dict[str, Any]:
        """Маппинг полей из входных данных.

        Args:
            data: Входные данные.

        Returns:
            Данные с переименованными полями.
        """
        if self.field_mapper is None:
            logger.warning("Маппер полей не инициализирован, поля не маппятся")
            return data

        return self.field_mapper.map_fields(data)

    def validate(self, data: dict[str, Any]) -> tuple[bool, list[str]]:
        """Валидация данных по текущей схеме.

        Args:
            data: Данные для валидации.

        Returns:
            Кортеж (валидны ли данные, список ошибок).
        """
        if self.validator is None:
            logger.warning("Валидатор не инициализирован, валидация пропущена")
            return True, []

        return self.validator.validate(data)

    def get_required_fields(self) -> list[str]:
        """Получение списка обязательных полей.

        Returns:
            Список обязательных полей.
        """
        if self.validator is None:
            return ["declaration_number", "date_issued", "declaration_type"]

        return self.validator.get_required_fields()

    def get_field_priority(self, field: str) -> str:
        """Получение приоритета поля.

        Args:
            field: Имя поля.

        Returns:
            Приоритет поля (P0, P1, P2).
        """
        if self.validator is None:
            p0_fields = ["declaration_number", "date_issued", "declaration_type"]
            return "P0" if field in p0_fields else "P2"

        return self.validator.get_field_priority(field)

    def get_schema_config(self) -> dict[str, Any] | None:
        """Получение текущей конфигурации схемы.

        Returns:
            Конфигурация схемы или None.
        """
        return self.current_schema

    def register_tenant_schema(self, tenant_id: str, schema_config: dict[str, Any]) -> None:
        """Регистрация новой схемы заказчика.

        Args:
            tenant_id: Идентификатор заказчика.
            schema_config: Конфигурация схемы.
        """
        self.registry.register_schema(tenant_id, schema_config)
        self.registry.save_schema(tenant_id, schema_config)

    def get_processing_config(self) -> dict[str, Any]:
        """Получение конфигурации обработки для текущего заказчика.

        Returns:
            Конфигурация обработки.
        """
        if self.current_schema is None:
            return {}

        return self.current_schema.get("processing", {})

    def get_search_config(self) -> dict[str, Any]:
        """Получение конфигурации поиска для текущего заказчика.

        Returns:
            Конфигурация поиска.
        """
        if self.current_schema is None:
            return {}

        return self.current_schema.get("search", {})
