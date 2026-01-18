"""Обработчик OCR результатов."""

import logging
from typing import Any

from dt_xml.ocr.field_extractor import FieldExtractor
from dt_xml.ocr.ocr_normalizer import OCRNormalizer
from dt_xml.schema.schema_manager import SchemaManager

logger = logging.getLogger(__name__)


class OCRProcessor:
    """Обработчик результатов OCR."""

    def __init__(self, schema_manager: SchemaManager | None = None):
        """Инициализация обработчика OCR.

        Args:
            schema_manager: Менеджер схем для маппинга полей.
        """
        self.field_extractor = FieldExtractor()
        self.normalizer = OCRNormalizer()
        self.schema_manager = schema_manager

    def process(
        self,
        ocr_text: str,
        tenant_id: str = "default",
        confidence_threshold: float = 0.7,
    ) -> dict[str, Any]:
        """Обработка OCR текста и извлечение структурированных данных.

        Args:
            ocr_text: Неструктурированный текст из OCR.
            tenant_id: Идентификатор заказчика.
            confidence_threshold: Порог уверенности (не используется в текущей реализации).

        Returns:
            Словарь со структурированными данными декларации.
        """
        if not ocr_text or not ocr_text.strip():
            logger.warning("Пустой OCR текст")
            return {}

        # Загрузка схемы заказчика, если доступна
        if self.schema_manager:
            try:
                self.schema_manager.load_tenant_schema(tenant_id)
            except Exception as e:
                logger.warning(f"Не удалось загрузить схему для {tenant_id}: {e}")

        # Извлечение полей из текста
        extracted_fields = self.field_extractor.extract_fields(ocr_text)

        # Нормализация извлеченных данных
        normalized_fields = self.normalizer.normalize(extracted_fields)

        # Добавление полного текста
        normalized_fields["full_text"] = ocr_text

        # Извлечение секций текста
        sections = self.field_extractor.extract_full_text_sections(ocr_text)
        normalized_fields["_sections"] = sections

        # Маппинг полей согласно схеме заказчика
        if self.schema_manager:
            try:
                normalized_fields = self.schema_manager.map_fields(normalized_fields)
            except Exception as e:
                logger.warning(f"Ошибка при маппинге полей: {e}")

        # Валидация обязательных полей
        if self.schema_manager:
            is_valid, errors = self.schema_manager.validate(normalized_fields)
            if not is_valid:
                logger.warning(f"Валидация не пройдена: {errors}")
                # Добавляем информацию об ошибках в результат
                normalized_fields["_validation_errors"] = errors

        logger.info(f"Извлечено {len(extracted_fields)} полей из OCR текста")

        return normalized_fields

    def extract_required_fields(self, ocr_text: str) -> dict[str, Any]:
        """Извлечение только обязательных полей.

        Args:
            ocr_text: Неструктурированный текст из OCR.

        Returns:
            Словарь с обязательными полями.
        """
        required_fields = ["declaration_number", "date_issued", "declaration_type"]
        extracted = self.field_extractor.extract_fields(ocr_text)

        result = {}
        for field in required_fields:
            if field in extracted:
                result[field] = extracted[field]

        return result

    def get_extraction_confidence(self, extracted_fields: dict[str, Any]) -> float:
        """Оценка уверенности в извлеченных данных.

        Args:
            extracted_fields: Извлеченные поля.

        Returns:
            Оценка уверенности от 0.0 до 1.0.
        """
        # Простая эвристика: чем больше полей извлечено, тем выше уверенность
        total_fields = len(extracted_fields)
        required_fields = ["declaration_number", "date_issued", "declaration_type"]

        # Базовая оценка
        confidence = min(total_fields / 10.0, 1.0)

        # Бонус за наличие обязательных полей
        required_count = sum(1 for field in required_fields if field in extracted_fields)
        confidence += (required_count / len(required_fields)) * 0.3

        return min(confidence, 1.0)
