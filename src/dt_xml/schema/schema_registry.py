"""Реестр схем заказчиков."""

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class SchemaRegistry:
    """Реестр схем данных для заказчиков."""

    def __init__(self, config_path: Path | None = None):
        """Инициализация реестра схем.

        Args:
            config_path: Путь к директории с конфигурациями заказчиков.
        """
        if config_path is None:
            config_path = Path("config/tenants")
        self.config_path = Path(config_path)
        self.schemas: dict[str, dict[str, Any]] = {}
        self._load_schemas()

    def _load_schemas(self) -> None:
        """Загрузка всех схем из конфигурационных файлов."""
        if not self.config_path.exists():
            logger.warning(f"Директория конфигураций не найдена: {self.config_path}")
            return

        for config_file in self.config_path.glob("*.yaml"):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    schema_config = yaml.safe_load(f)

                tenant_id = schema_config.get("tenant_id", config_file.stem)
                self.schemas[tenant_id] = schema_config
                logger.info(f"Загружена схема для заказчика: {tenant_id}")

            except Exception as e:
                logger.error(f"Ошибка при загрузке схемы из {config_file}: {e}")

    def get_schema(self, tenant_id: str) -> dict[str, Any] | None:
        """Получение схемы для заказчика.

        Args:
            tenant_id: Идентификатор заказчика.

        Returns:
            Конфигурация схемы или None.
        """
        # Если схема не найдена, возвращаем схему по умолчанию
        if tenant_id not in self.schemas:
            logger.warning(f"Схема для заказчика {tenant_id} не найдена, используется default")
            return self.schemas.get("default")

        return self.schemas.get(tenant_id)

    def register_schema(self, tenant_id: str, schema_config: dict[str, Any]) -> None:
        """Регистрация новой схемы.

        Args:
            tenant_id: Идентификатор заказчика.
            schema_config: Конфигурация схемы.
        """
        self.schemas[tenant_id] = schema_config
        logger.info(f"Зарегистрирована схема для заказчика: {tenant_id}")

    def save_schema(self, tenant_id: str, schema_config: dict[str, Any]) -> None:
        """Сохранение схемы в файл.

        Args:
            tenant_id: Идентификатор заказчика.
            schema_config: Конфигурация схемы.
        """
        self.config_path.mkdir(parents=True, exist_ok=True)
        config_file = self.config_path / f"{tenant_id}.yaml"

        try:
            with open(config_file, "w", encoding="utf-8") as f:
                yaml.dump(schema_config, f, allow_unicode=True, default_flow_style=False)

            self.schemas[tenant_id] = schema_config
            logger.info(f"Схема сохранена в {config_file}")

        except Exception as e:
            logger.error(f"Ошибка при сохранении схемы: {e}")
            raise

    def list_tenants(self) -> list[str]:
        """Получение списка всех заказчиков.

        Returns:
            Список идентификаторов заказчиков.
        """
        return list(self.schemas.keys())

    def reload(self) -> None:
        """Перезагрузка всех схем из файлов."""
        self.schemas.clear()
        self._load_schemas()
