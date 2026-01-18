# Use Cases

## Use Case 1: Preparing a New Declaration

### Scenario
An employee is preparing a declaration for importing Samsung smartphones.

### Without DT-XML
1. Search database by manufacturer (30 minutes)
2. Review found declarations (1 hour)
3. Select suitable example (30 minutes)
4. Copy formulations (30 minutes)
5. Verify compliance (30 minutes)
**Total**: 2.5 hours

### With DT-XML
1. Search: "Samsung smartphones 2023" (5 seconds)
2. Review top-5 results (2 minutes)
3. Copy formulations (5 minutes)
**Total**: 7 minutes

**Time saved**: 2 hours 23 minutes (94% reduction)

### Code Example

```python
import requests

# Search for similar declarations
response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "Samsung smartphones 2023",
        "tenant_id": "default",
        "top_k": 5,
        "filters": {
            "manufacturer": "Samsung",
            "date_issued": {"gte": "2023-01-01"}
        },
        "explain": True
    }
)

results = response.json()["results"]
for result in results:
    print(f"Declaration: {result['declaration_id']}")
    print(f"Relevance: {result['score']:.2f}")
    print(f"Reason: {result['explanation']['reasons']}")
    print(f"Content: {result['content'][:200]}...")
    print("---")
```

## Use Case 2: Verifying HS Code Correctness

### Scenario
Need to verify if the HS code is correctly specified for a product.

### Without DT-XML
- Manual search by code in database
- Check product descriptions
- Consult with expert
**Time**: 1-2 hours

### With DT-XML
- Search by HS code
- View examples with similar descriptions
- Automatic comparison
**Time**: 5 minutes

**Time saved**: 1 hour 55 minutes (96% reduction)

### Code Example

```python
# Search by HS code and product description
response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "smartphones mobile phones",
        "tenant_id": "default",
        "top_k": 10,
        "filters": {"product_code": "8517120000"},
        "explain": True
    }
)

# Check if descriptions match
for result in response.json()["results"]:
    if "smartphone" in result["content"].lower():
        print(f"✓ Found matching declaration: {result['declaration_id']}")
        print(f"  HS Code: {result['metadata'].get('product_code')}")
        print(f"  Description: {result['content'][:100]}...")
```

## Use Case 3: Finding Historical Precedents

### Scenario
Need to find all declarations for a specific manufacturer over the past year to understand patterns.

### Code Example

```python
import requests
from datetime import datetime, timedelta

# Search for all declarations in the past year
one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "Apple products",
        "tenant_id": "default",
        "top_k": 100,
        "filters": {
            "manufacturer": "Apple",
            "date_issued": {"gte": one_year_ago}
        }
    }
)

results = response.json()["results"]
print(f"Found {len(results)} declarations for Apple in the past year")

# Group by product code
product_codes = {}
for result in results:
    code = result["metadata"].get("product_code", "unknown")
    if code not in product_codes:
        product_codes[code] = []
    product_codes[code].append(result["declaration_id"])

print("\nDeclarations by HS code:")
for code, declarations in product_codes.items():
    print(f"  {code}: {len(declarations)} declarations")
```

## Use Case 4: Batch Indexing

### Scenario
Index multiple declarations from a directory.

### Code Example

```python
import os
import requests
from pathlib import Path

def index_directory(directory_path: str, tenant_id: str = "default"):
    """Index all XML files in a directory."""
    directory = Path(directory_path)
    indexed = 0
    errors = 0
    
    for xml_file in directory.glob("*.xml"):
        try:
            with open(xml_file, "r", encoding="utf-8") as f:
                xml_content = f.read()
            
            response = requests.post(
                "http://localhost:8000/index",
                json={
                    "tenant_id": tenant_id,
                    "xml_content": xml_content
                }
            )
            
            if response.status_code == 200:
                indexed += 1
                print(f"✓ Indexed: {xml_file.name}")
            else:
                errors += 1
                print(f"✗ Error indexing {xml_file.name}: {response.text}")
                
        except Exception as e:
            errors += 1
            print(f"✗ Error reading {xml_file.name}: {e}")
    
    print(f"\nIndexed: {indexed}, Errors: {errors}")

# Usage
index_directory("data/raw/declarations", tenant_id="default")
```

## Use Case 5: Tenant-Specific Schema

### Scenario
Different logistics company has different field names in their declarations.

### Code Example

```python
# Register custom schema for tenant
schema_config = {
    "tenant_id": "logistics_company_1",
    "tenant_name": "Logistics Company 1",
    "schema": {
        "field_mapping": {
            "declaration_number": ["number", "declaration_id"],
            "manufacturer": ["producer", "manufacturer_name"],
            "product_code": ["hs_code", "tn_ved_code"]
        },
        "required_for_search": [
            "declaration_number",
            "date_issued",
            "manufacturer",
            "product_code"
        ]
    },
    "processing": {
        "ocr_enabled": True,
        "auto_normalize": True
    },
    "search": {
        "boost_fields": {
            "manufacturer": 2.0,
            "product_code": 1.5
        }
    }
}

# Register schema
response = requests.post(
    "http://localhost:8000/schema/register",
    json=schema_config
)

print(f"Schema registered: {response.json()['status']}")

# Now use tenant-specific schema
response = requests.post(
    "http://localhost:8000/index",
    json={
        "tenant_id": "logistics_company_1",
        "json_data": {
            "number": "12345",  # Will be mapped to declaration_number
            "producer": "Samsung",  # Will be mapped to manufacturer
            "hs_code": "8517120000"  # Will be mapped to product_code
        }
    }
)
```
