# API Спецификация

## Базовый URL

```
http://localhost:8000
```

## Эндпоинты

### Health Check

#### GET /health или GET /healthz

Проверка состояния сервиса.

**Ответ:**
```json
{
  "status": "healthy",
  "vector_db": {
    "name": "declarations",
    "vectors_count": 1000,
    "vector_size": 1024
  },
  "metadata_db": {
    "status": "connected"
  },
  "embedding_model": {
    "model_name": "BAAI/bge-m3",
    "embedding_dimension": 1024
  }
}
```

### Поиск

#### POST /search

Поиск по декларациям.

**Запрос:**
```json
{
  "query": "производитель Samsung, товар телефоны, 2023 год",
  "top_k": 10,
  "filters": {
    "date_issued": {
      "gte": "2023-01-01",
      "lte": "2023-12-31"
    },
    "manufacturer": "Samsung"
  },
  "rerank": true,
  "explain": true
}
```

**Ответ:**
```json
{
  "results": [
    {
      "declaration_id": "12345",
      "chunk_id": "chunk-1",
      "content": "Описание товара...",
      "score": 0.95,
      "metadata": {
        "manufacturer": "Samsung",
        "date_issued": "2023-06-15",
        "product_code": "8517120000"
      },
      "explanation": {
        "relevance_score": 0.95,
        "matched_fields": ["manufacturer", "content"],
        "matched_terms": ["samsung", "телефоны"],
        "reasons": [
          "Совпадение в поле 'manufacturer'",
          "Найдены совпадающие термины: samsung, телефоны"
        ]
      },
      "matched_fields": ["manufacturer", "content"]
    }
  ],
  "total": 1,
  "query_time_ms": 45.2,
  "query": "производитель Samsung, товар телефоны, 2023 год"
}
```

### Индексация

#### POST /index

Индексация новой декларации.

**Запрос:**
```json
{
  "declaration_id": "12345",
  "xml_content": "<declaration>...</declaration>"
}
```

или

```json
{
  "declaration_id": "12345",
  "json_data": {
    "declaration_number": "12345",
    "date_issued": "2023-06-15",
    "manufacturer": "Samsung",
    ...
  }
}
```

**Ответ:**
```json
{
  "declaration_id": "12345",
  "chunks_count": 5,
  "indexed_at": "2024-01-15T10:30:00",
  "status": "success"
}
```

## Коды ошибок

- `400` - Неверный запрос
- `500` - Внутренняя ошибка сервера
