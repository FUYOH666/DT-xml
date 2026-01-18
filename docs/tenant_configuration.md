# Настройка схем заказчиков

## Обзор

Система поддерживает платформенную архитектуру с динамическими схемами данных для каждого заказчика. Это позволяет:

- Настраивать маппинг полей из входного формата в внутренний
- Определять обязательные поля для поиска
- Добавлять кастомные поля
- Настраивать параметры обработки и поиска

## Структура конфигурации

Конфигурации заказчиков хранятся в `config/tenants/` в формате YAML:

```yaml
tenant_id: "tenant_1"
tenant_name: "Заказчик 1"

schema:
  # Маппинг полей из входного формата
  field_mapping:
    declaration_number:
      - "declaration_number"
      - "number"
      - "номер"
    manufacturer:
      - "manufacturer"
      - "producer"
      - "производитель"
    # ...

  # Обязательные поля для поиска
  required_for_search:
    - declaration_number
    - date_issued
    - manufacturer
    - product_code
    - product_description

  # Типы полей для валидации
  field_types:
    declaration_number: "string"
    date_issued: "date"
    customs_value: "number"

  # Кастомные поля
  custom_fields:
    - field_name: "custom_field_1"
      type: "string"
      searchable: true

# Настройки обработки
processing:
  ocr_enabled: true
  ocr_confidence_threshold: 0.7
  auto_normalize: true

# Настройки поиска
search:
  default_filters:
    - manufacturer
    - product_code
  boost_fields:
    manufacturer: 2.0
    product_code: 1.5
```

## Регистрация схемы через API

Схему можно зарегистрировать через API:

```bash
POST /api/v1/schema/register
Content-Type: application/json

{
  "tenant_id": "tenant_1",
  "tenant_name": "Заказчик 1",
  "schema": {
    "field_mapping": {
      "declaration_number": ["number", "номер"],
      "manufacturer": ["producer", "производитель"]
    },
    "required_for_search": [
      "declaration_number",
      "date_issued",
      "manufacturer"
    ]
  },
  "processing": {
    "ocr_enabled": true
  },
  "search": {
    "boost_fields": {
      "manufacturer": 2.0
    }
  }
}
```

## Использование схемы

После регистрации схемы, укажите `tenant_id` в запросах:

```bash
POST /api/v1/index
{
  "tenant_id": "tenant_1",
  "xml_content": "..."
}
```

Система автоматически:
1. Загрузит схему заказчика
2. Применит маппинг полей
3. Валидирует обязательные поля
4. Использует настройки обработки и поиска

## Маппинг полей

Маппинг позволяет преобразовать поля из входного формата в стандартный внутренний формат:

```yaml
field_mapping:
  declaration_number:
    - "declaration_number"  # Стандартное имя
    - "number"              # Альтернативное имя
    - "номер"               # Русское имя
```

Система будет искать поле по всем указанным именам и использовать первое найденное значение.

## Обязательные поля для поиска

Определите минимальный набор полей, необходимых для эффективного поиска:

```yaml
required_for_search:
  - declaration_number  # P0 - обязательное
  - date_issued         # P0 - обязательное
  - declaration_type    # P0 - обязательное
  - manufacturer        # P1 - критичное для поиска
  - product_code        # P1 - критичное для поиска
  - product_description # P1 - критичное для поиска
```

## Кастомные поля

Можно добавить дополнительные поля, специфичные для заказчика:

```yaml
custom_fields:
  - field_name: "internal_code"
    type: "string"
    searchable: true
  - field_name: "department"
    type: "string"
    searchable: false
```

## Настройки обработки

```yaml
processing:
  ocr_enabled: true                    # Включить поддержку OCR
  ocr_confidence_threshold: 0.7        # Порог уверенности OCR
  auto_normalize: true                 # Автоматическая нормализация
  language_detection: true             # Определение языка
```

## Настройки поиска

```yaml
search:
  default_filters:                    # Фильтры по умолчанию
    - manufacturer
    - product_code
  boost_fields:                        # Усиление важных полей
    manufacturer: 2.0
    product_code: 1.5
    product_description: 1.2
```

## Примеры

### Пример 1: Базовая схема

```yaml
tenant_id: "simple_tenant"
tenant_name: "Простой заказчик"

schema:
  field_mapping:
    declaration_number: ["number"]
    date_issued: ["date"]
    manufacturer: ["producer"]
  required_for_search:
    - declaration_number
    - date_issued
    - manufacturer
```

### Пример 2: Расширенная схема с кастомными полями

```yaml
tenant_id: "advanced_tenant"
tenant_name: "Продвинутый заказчик"

schema:
  field_mapping:
    declaration_number: ["number", "declaration_id"]
    manufacturer: ["producer", "manufacturer_name"]
  required_for_search:
    - declaration_number
    - date_issued
    - manufacturer
    - product_code
  custom_fields:
    - field_name: "contract_number"
      type: "string"
      searchable: true
    - field_name: "approval_date"
      type: "date"
      searchable: false

processing:
  ocr_enabled: true
  auto_normalize: true

search:
  boost_fields:
    manufacturer: 3.0
    contract_number: 1.5
```

## Получение схемы

```bash
GET /api/v1/schema/{tenant_id}
```

## Список всех схем

```bash
GET /api/v1/schema/
```
