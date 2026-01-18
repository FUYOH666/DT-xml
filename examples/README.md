# Examples and Use Cases

This directory contains examples of using DT-XML for various scenarios.

## Structure

- `data/` - Sample customs declarations in different formats
- `scripts/` - Example scripts for common tasks
- `api_examples/` - API usage examples

## Quick Examples

### Example 1: Search by Manufacturer

Find all declarations for a specific manufacturer:

```python
import requests

response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "Samsung smartphones",
        "tenant_id": "default",
        "top_k": 10,
        "filters": {
            "manufacturer": "Samsung",
            "date_issued": {"gte": "2023-01-01", "lte": "2023-12-31"}
        }
    }
)

for result in response.json()["results"]:
    print(f"Declaration: {result['declaration_id']}")
    print(f"Score: {result['score']}")
    print(f"Manufacturer: {result['metadata'].get('manufacturer')}")
    print("---")
```

### Example 2: Search by HS Code

Find declarations with a specific HS code:

```python
response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "8517120000",
        "tenant_id": "default",
        "top_k": 5,
        "filters": {"product_code": "8517120000"}
    }
)
```

### Example 3: Index XML Declaration

Index a new declaration from XML:

```python
xml_content = """
<declaration>
    <declaration_number>12345</declaration_number>
    <date_issued>2023-06-15</date_issued>
    <declaration_type>import</declaration_type>
    <manufacturer>Samsung Electronics</manufacturer>
    <product_code>8517120000</product_code>
    <product_description>Smartphones with 5G support</product_description>
    <country_origin>CN</country_origin>
    <customs_value>1000000</customs_value>
    <currency>USD</currency>
</declaration>
"""

response = requests.post(
    "http://localhost:8000/index",
    json={
        "tenant_id": "default",
        "xml_content": xml_content
    }
)

print(f"Indexed declaration: {response.json()['declaration_id']}")
```

### Example 4: Process OCR Text

Index a declaration from OCR text:

```python
ocr_text = """
Номер декларации: 12345
Дата выпуска: 15.06.2023
Производитель: Samsung Electronics
Код товара: 8517120000
Описание: Смартфоны с поддержкой 5G
Страна происхождения: CN
Таможенная стоимость: 1000000 USD
"""

response = requests.post(
    "http://localhost:8000/index",
    json={
        "tenant_id": "default",
        "ocr_text": ocr_text
    }
)
```

## Use Cases

See [USE_CASES.md](USE_CASES.md) for detailed business use cases.
