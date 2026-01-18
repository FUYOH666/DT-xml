"""Парсер XML деклараций ЕАЭС."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import xmltodict
from lxml import etree

from dt_xml.config.models import DeclarationMetadata, DeclarationType, DeclarationStatus
from dt_xml.parser.schema_validator import SchemaValidator
from dt_xml.schema.schema_manager import SchemaManager

logger = logging.getLogger(__name__)


class XMLParser:
    """Парсер XML деклараций ЕАЭС."""

    def __init__(self, schema_path: Path | None = None, schema_manager: SchemaManager | None = None):
        """Инициализация парсера.

        Args:
            schema_path: Путь к XSD схеме для валидации (legacy).
            schema_manager: Менеджер схем для динамических схем заказчиков.
        """
        self.validator = SchemaValidator(schema_path)
        self.schema_manager = schema_manager

    def parse_file(self, file_path: Path, tenant_id: str = "default") -> dict[str, Any]:
        """Парсинг XML файла.

        Args:
            file_path: Путь к XML файлу.
            tenant_id: Идентификатор заказчика для загрузки схемы.

        Returns:
            Словарь с распарсенными данными декларации.

        Raises:
            ValueError: Если файл не может быть распарсен.
        """
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            return self.parse(content, tenant_id=tenant_id)
        except Exception as e:
            logger.error(f"Ошибка при чтении файла {file_path}: {e}")
            raise ValueError(f"Не удалось прочитать файл {file_path}: {e}") from e

    def parse(
        self,
        xml_content: str | bytes,
        tenant_id: str = "default",
    ) -> dict[str, Any]:
        """Парсинг XML контента.

        Args:
            xml_content: XML контент для парсинга.
            tenant_id: Идентификатор заказчика для загрузки схемы.

        Returns:
            Словарь с распарсенными данными декларации.

        Raises:
            ValueError: Если контент не может быть распарсен.
        """
        try:
            # Загрузка схемы заказчика, если доступен SchemaManager
            if self.schema_manager:
                try:
                    self.schema_manager.load_tenant_schema(tenant_id)
                except Exception as e:
                    logger.warning(f"Не удалось загрузить схему для {tenant_id}: {e}")

            # Валидация (legacy XSD валидация)
            is_valid, errors = self.validator.validate(xml_content)
            if not is_valid:
                logger.warning(f"XML не прошел валидацию: {errors}")

            # Парсинг через xmltodict для удобной работы со структурой
            if isinstance(xml_content, str):
                xml_content = xml_content.encode("utf-8")

            parsed_dict = xmltodict.parse(xml_content, process_namespaces=True)

            # Извлечение данных декларации
            declaration_data = self._extract_declaration_data(parsed_dict)

            # Маппинг полей согласно схеме заказчика
            if self.schema_manager:
                try:
                    declaration_data = self.schema_manager.map_fields(declaration_data)
                except Exception as e:
                    logger.warning(f"Ошибка при маппинге полей: {e}")

            # Валидация обязательных полей для поиска
            if self.schema_manager:
                is_valid, errors = self.schema_manager.validate(declaration_data)
                if not is_valid:
                    logger.warning(f"Валидация обязательных полей не пройдена: {errors}")
                    declaration_data["_validation_errors"] = errors

            return declaration_data

        except Exception as e:
            logger.error(f"Ошибка при парсинге XML: {e}")
            raise ValueError(f"Не удалось распарсить XML: {e}") from e

    def _extract_declaration_data(self, parsed_dict: dict[str, Any]) -> dict[str, Any]:
        """Извлечение данных декларации из распарсенного словаря.

        Args:
            parsed_dict: Словарь, полученный из xmltodict.

        Returns:
            Словарь с извлеченными данными декларации.
        """
        # Поиск корневого элемента декларации
        # Структура может варьироваться в зависимости от версии схемы ЕАЭС
        root_key = self._find_declaration_root(parsed_dict)
        declaration_root = parsed_dict.get(root_key, parsed_dict)

        # Извлечение основных полей
        data: dict[str, Any] = {}

        # Номер декларации
        data["declaration_number"] = self._extract_field(
            declaration_root,
            ["declaration_number", "declarationNumber", "НомерДекларации", "number"],
        )

        # Дата выпуска
        date_str = self._extract_field(
            declaration_root,
            ["date_issued", "dateIssued", "ДатаВыпуска", "date", "issue_date"],
        )
        data["date_issued"] = self._parse_date(date_str) if date_str else None

        # Тип декларации
        decl_type = self._extract_field(
            declaration_root,
            ["declaration_type", "declarationType", "ТипДекларации", "type"],
        )
        data["declaration_type"] = self._parse_declaration_type(decl_type)

        # Статус
        status = self._extract_field(
            declaration_root,
            ["status", "Статус", "state"],
        )
        data["status"] = self._parse_status(status)

        # Производитель
        data["manufacturer"] = self._extract_field(
            declaration_root,
            ["manufacturer", "Производитель", "producer", "producer_name"],
        )

        # Импортер
        data["importer"] = self._extract_field(
            declaration_root,
            ["importer", "Импортер", "importer_name", "consignee"],
        )

        # Экспортер
        data["exporter"] = self._extract_field(
            declaration_root,
            ["exporter", "Экспортер", "exporter_name", "consignor"],
        )

        # Код товара (ТН ВЭД)
        data["product_code"] = self._extract_field(
            declaration_root,
            ["product_code", "productCode", "КодТовара", "tn_ved", "hs_code"],
        )

        # Описание товара
        data["product_description"] = self._extract_field(
            declaration_root,
            ["product_description", "productDescription", "ОписаниеТовара", "description"],
        )

        # Страна происхождения
        data["country_origin"] = self._extract_field(
            declaration_root,
            ["country_origin", "countryOrigin", "СтранаПроисхождения", "origin_country"],
        )

        # Таможенная стоимость
        value_str = self._extract_field(
            declaration_root,
            ["customs_value", "customsValue", "ТаможеннаяСтоимость", "value"],
        )
        data["customs_value"] = self._parse_float(value_str)

        # Валюта
        data["currency"] = self._extract_field(
            declaration_root,
            ["currency", "Валюта", "currency_code"],
        )

        # Количество
        qty_str = self._extract_field(
            declaration_root,
            ["quantity", "Количество", "qty", "amount"],
        )
        data["quantity"] = self._parse_float(qty_str)

        # Единица измерения
        data["unit_of_measure"] = self._extract_field(
            declaration_root,
            ["unit_of_measure", "unitOfMeasure", "ЕдиницаИзмерения", "unit"],
        )

        # Полный текст декларации (для поиска)
        data["full_text"] = self._extract_full_text(declaration_root)

        # Метаданные
        data["language"] = self._detect_language(data.get("full_text", ""))
        data["version"] = self._extract_field(
            declaration_root,
            ["version", "Версия", "schema_version"],
            default="1.0",
        )
        data["source"] = self._extract_field(
            declaration_root,
            ["source", "Источник", "source_system"],
        )

        # Сохранение оригинальной структуры для дальнейшей обработки
        data["_raw_data"] = declaration_root

        return data

    def _find_declaration_root(self, parsed_dict: dict[str, Any]) -> str:
        """Поиск корневого элемента декларации.

        Args:
            parsed_dict: Распарсенный словарь.

        Returns:
            Ключ корневого элемента.
        """
        # Возможные названия корневых элементов
        possible_roots = [
            "declaration",
            "Declaration",
            "Декларация",
            "customs_declaration",
            "CustomsDeclaration",
        ]

        for root in possible_roots:
            if root in parsed_dict:
                return root

        # Если не найден, возвращаем первый ключ верхнего уровня
        if parsed_dict:
            return list(parsed_dict.keys())[0]

        return ""

    def _extract_field(
        self,
        data: dict[str, Any],
        possible_keys: list[str],
        default: str | None = None,
    ) -> str | None:
        """Извлечение поля по возможным ключам.

        Args:
            data: Словарь данных.
            possible_keys: Список возможных ключей.
            default: Значение по умолчанию.

        Returns:
            Значение поля или None.
        """
        for key in possible_keys:
            value = self._get_nested_value(data, key)
            if value is not None:
                if isinstance(value, (dict, list)):
                    # Если значение - сложная структура, преобразуем в строку
                    return str(value)
                return str(value).strip() if value else None

        return default

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

    def _parse_date(self, date_str: str | None) -> datetime | None:
        """Парсинг даты из строки.

        Args:
            date_str: Строка с датой.

        Returns:
            Объект datetime или None.
        """
        if not date_str:
            return None

        # Различные форматы дат
        formats = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%d.%m.%Y",
            "%d/%m/%Y",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue

        logger.warning(f"Не удалось распарсить дату: {date_str}")
        return None

    def _parse_float(self, value_str: str | None) -> float | None:
        """Парсинг числа с плавающей точкой.

        Args:
            value_str: Строка с числом.

        Returns:
            Число или None.
        """
        if not value_str:
            return None

        try:
            # Удаление пробелов и замены запятой на точку
            cleaned = str(value_str).strip().replace(",", ".").replace(" ", "")
            return float(cleaned)
        except (ValueError, AttributeError):
            return None

    def _parse_declaration_type(self, type_str: str | None) -> DeclarationType:
        """Парсинг типа декларации.

        Args:
            type_str: Строка с типом.

        Returns:
            Enum типа декларации.
        """
        if not type_str:
            return DeclarationType.IMPORT

        type_lower = str(type_str).lower()
        if "export" in type_lower or "экспорт" in type_lower:
            return DeclarationType.EXPORT
        elif "transit" in type_lower or "транзит" in type_lower:
            return DeclarationType.TRANSIT
        else:
            return DeclarationType.IMPORT

    def _parse_status(self, status_str: str | None) -> DeclarationStatus:
        """Парсинг статуса декларации.

        Args:
            status_str: Строка со статусом.

        Returns:
            Enum статуса декларации.
        """
        if not status_str:
            return DeclarationStatus.REGISTERED

        status_lower = str(status_str).lower()
        if "released" in status_lower or "выпущен" in status_lower:
            return DeclarationStatus.RELEASED
        elif "rejected" in status_lower or "отказ" in status_lower:
            return DeclarationStatus.REJECTED
        elif "corrected" in status_lower or "исправлен" in status_lower:
            return DeclarationStatus.CORRECTED
        else:
            return DeclarationStatus.REGISTERED

    def _extract_full_text(self, data: dict[str, Any]) -> str:
        """Извлечение полного текста декларации.

        Args:
            data: Словарь данных декларации.

        Returns:
            Полный текст декларации.
        """
        text_parts: list[str] = []

        def extract_text_recursive(obj: Any) -> None:
            """Рекурсивное извлечение текста."""
            if isinstance(obj, dict):
                for value in obj.values():
                    extract_text_recursive(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_text_recursive(item)
            elif isinstance(obj, str):
                text_parts.append(obj)

        extract_text_recursive(data)
        return " ".join(text_parts)

    def _detect_language(self, text: str) -> str:
        """Определение языка текста.

        Args:
            text: Текст для определения языка.

        Returns:
            Код языка (ru, kz, en и т.д.).
        """
        if not text:
            return "ru"

        # Простая эвристика (в реальной реализации использовать langdetect)
        text_lower = text.lower()
        if any(char in text_lower for char in "әіңғұүқөһ"):
            return "kz"  # Казахский
        elif any(ord(char) > 127 for char in text[:100]):
            return "ru"  # Русский (кириллица)
        else:
            return "en"  # Английский

    def to_metadata(self, parsed_data: dict[str, Any]) -> DeclarationMetadata:
        """Преобразование распарсенных данных в метаданные.

        Args:
            parsed_data: Распарсенные данные декларации.

        Returns:
            Объект метаданных декларации.
        """
        return DeclarationMetadata(
            declaration_number=parsed_data.get("declaration_number", ""),
            date_issued=parsed_data.get("date_issued") or datetime.now(),
            declaration_type=parsed_data.get("declaration_type", DeclarationType.IMPORT),
            status=parsed_data.get("status", DeclarationStatus.REGISTERED),
            manufacturer=parsed_data.get("manufacturer"),
            importer=parsed_data.get("importer"),
            exporter=parsed_data.get("exporter"),
            product_code=parsed_data.get("product_code"),
            country_origin=parsed_data.get("country_origin"),
            customs_value=parsed_data.get("customs_value"),
            currency=parsed_data.get("currency"),
            quantity=parsed_data.get("quantity"),
            unit_of_measure=parsed_data.get("unit_of_measure"),
            language=parsed_data.get("language", "ru"),
            version=parsed_data.get("version", "1.0"),
            source=parsed_data.get("source"),
            processed_at=datetime.now(),
        )
