# Формат данных для клиентов

## Требования к входным данным

Система принимает таможенные декларации ЕАЭС в следующих форматах:

### 1. XML формат (стандарт ЕАЭС)

Декларации должны быть в формате XML с обязательными полями:

```xml
<declaration>
  <declaration_number>12345</declaration_number>
  <date_issued>2023-06-15</date_issued>
  <declaration_type>import</declaration_type>
  <manufacturer>Samsung Electronics</manufacturer>
  <importer>ООО "Импортер"</importer>
  <product_code>8517120000</product_code>
  <product_description>Смартфоны</product_description>
  <country_origin>CN</country_origin>
  <customs_value>1000000</customs_value>
  <currency>USD</currency>
  <quantity>1000</quantity>
  <unit_of_measure>шт</unit_of_measure>
</declaration>
```

### 2. JSON формат

Альтернативный формат для структурированных данных:

```json
{
  "declaration_number": "12345",
  "date_issued": "2023-06-15",
  "declaration_type": "import",
  "manufacturer": "Samsung Electronics",
  "importer": "ООО \"Импортер\"",
  "product_code": "8517120000",
  "product_description": "Смартфоны",
  "country_origin": "CN",
  "customs_value": 1000000,
  "currency": "USD",
  "quantity": 1000,
  "unit_of_measure": "шт"
}
```

## Обязательные поля для поиска

Система использует трехуровневую систему приоритетов полей. Подробнее см. [Обязательные поля для поиска](mandatory_fields.md).

### P0 - Обязательные (критичные для работы системы)

- `declaration_number` - Номер декларации
- `date_issued` - Дата выпуска (формат: YYYY-MM-DD)
- `declaration_type` - Тип декларации (import/export/transit)

**Без этих полей система не сможет корректно обработать декларацию.**

### P1 - Критичные для поиска (рекомендуемые)

- `manufacturer` - Производитель (основной критерий поиска)
- `product_code` - Код товара (ТН ВЭД, 10 цифр) - точный поиск
- `product_description` - Описание товара - семантический поиск
- `full_text` - Полный текст декларации - для embedding

**Без этих полей поиск будет работать с ограниченной точностью.**

### P2 - Желательные (опциональные)

- `manufacturer` - Производитель
- `importer` - Импортер
- `exporter` - Экспортер
- `product_code` - Код товара (ТН ВЭД, 10 цифр)
- `product_description` - Описание товара
- `country_origin` - Страна происхождения (ISO код)
- `customs_value` - Таможенная стоимость
- `currency` - Валюта (ISO код)
- `quantity` - Количество
- `unit_of_measure` - Единица измерения

## Метаданные

- `version` - Версия декларации (по умолчанию "1.0")
- `source` - Источник данных
- `language` - Язык документа (ru/kz/en)

## Требования к качеству данных

1. **Кодировка**: UTF-8
2. **Нормализация**: Названия компаний должны быть в едином формате
3. **Коды**: Коды ТН ВЭД должны быть в формате 10 цифр
4. **Даты**: Формат YYYY-MM-DD или ISO 8601
5. **Валюты**: ISO 4217 коды (USD, EUR, RUB и т.д.)
6. **Страны**: ISO 3166-1 alpha-2 коды (RU, KZ, CN и т.д.)

## Поддержка OCR (fallback)

Система поддерживает обработку неструктурированного текста из OCR как альтернативный формат входных данных:

```json
{
  "ocr_text": "Номер декларации: 12345\nДата выпуска: 15.06.2023\nПроизводитель: Samsung Electronics\n..."
}
```

Система автоматически извлечет поля из OCR текста, но качество будет зависеть от структуры текста.

## Платформенная архитектура

Система поддерживает динамические схемы данных для разных заказчиков. Каждый заказчик может иметь свою схему с маппингом полей. Подробнее см. [Настройка схем заказчиков](tenant_configuration.md).

## Примеры

См. директорию `data/examples/` для примеров деклараций.
