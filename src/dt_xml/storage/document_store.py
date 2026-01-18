"""Хранилище оригинальных документов."""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from dt_xml.config.settings import get_settings

logger = logging.getLogger(__name__)


class DocumentStore:
    """Хранилище оригинальных документов деклараций."""

    def __init__(self, storage_path: Path | None = None):
        """Инициализация хранилища документов.

        Args:
            storage_path: Путь к директории хранения. Если None, используется из настроек.
        """
        self.settings = get_settings()
        if storage_path is None:
            storage_path = Path("data/processed/documents")
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save_document(
        self,
        declaration_id: str,
        content: str | dict[str, Any],
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Сохранение документа декларации.

        Args:
            declaration_id: Идентификатор декларации.
            content: Содержимое документа (текст или словарь).
            metadata: Дополнительные метаданные.

        Returns:
            Путь к сохраненному файлу.
        """
        try:
            # Создание поддиректории по первым символам ID для организации
            subdir = declaration_id[:2] if len(declaration_id) >= 2 else "00"
            doc_dir = self.storage_path / subdir
            doc_dir.mkdir(parents=True, exist_ok=True)

            # Путь к файлу
            file_path = doc_dir / f"{declaration_id}.json"

            # Подготовка данных для сохранения
            document_data = {
                "declaration_id": declaration_id,
                "content": content,
                "metadata": metadata or {},
                "saved_at": datetime.utcnow().isoformat(),
            }

            # Сохранение в JSON
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(document_data, f, ensure_ascii=False, indent=2)

            logger.info(f"Документ {declaration_id} сохранен в {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"Ошибка при сохранении документа {declaration_id}: {e}")
            raise

    def get_document(self, declaration_id: str) -> dict[str, Any] | None:
        """Получение документа декларации.

        Args:
            declaration_id: Идентификатор декларации.

        Returns:
            Словарь с данными документа или None.
        """
        try:
            # Поиск файла
            subdir = declaration_id[:2] if len(declaration_id) >= 2 else "00"
            file_path = self.storage_path / subdir / f"{declaration_id}.json"

            if not file_path.exists():
                logger.warning(f"Документ {declaration_id} не найден")
                return None

            # Загрузка из JSON
            with open(file_path, "r", encoding="utf-8") as f:
                document_data = json.load(f)

            return document_data

        except Exception as e:
            logger.error(f"Ошибка при получении документа {declaration_id}: {e}")
            return None

    def delete_document(self, declaration_id: str) -> None:
        """Удаление документа декларации.

        Args:
            declaration_id: Идентификатор декларации.
        """
        try:
            subdir = declaration_id[:2] if len(declaration_id) >= 2 else "00"
            file_path = self.storage_path / subdir / f"{declaration_id}.json"

            if file_path.exists():
                file_path.unlink()
                logger.info(f"Документ {declaration_id} удален")
            else:
                logger.warning(f"Документ {declaration_id} не найден для удаления")

        except Exception as e:
            logger.error(f"Ошибка при удалении документа {declaration_id}: {e}")
            raise

    def list_documents(self, limit: int = 100) -> list[str]:
        """Получение списка идентификаторов документов.

        Args:
            limit: Максимальное количество идентификаторов.

        Returns:
            Список идентификаторов деклараций.
        """
        declaration_ids = []

        try:
            # Обход всех поддиректорий
            for subdir in self.storage_path.iterdir():
                if subdir.is_dir():
                    for file_path in subdir.glob("*.json"):
                        declaration_id = file_path.stem
                        declaration_ids.append(declaration_id)

                        if len(declaration_ids) >= limit:
                            break

                if len(declaration_ids) >= limit:
                    break

        except Exception as e:
            logger.error(f"Ошибка при получении списка документов: {e}")

        return declaration_ids[:limit]
