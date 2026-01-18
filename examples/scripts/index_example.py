#!/usr/bin/env python3
"""Example script for indexing declarations."""

import requests
import json
from pathlib import Path

API_BASE_URL = "http://localhost:8000"


def index_xml(xml_content: str, tenant_id: str = "default", declaration_id: str | None = None):
    """Index a declaration from XML.
    
    Args:
        xml_content: XML content of the declaration
        tenant_id: Tenant identifier
        declaration_id: Optional declaration ID
    """
    response = requests.post(
        f"{API_BASE_URL}/index",
        json={
            "declaration_id": declaration_id,
            "tenant_id": tenant_id,
            "xml_content": xml_content
        }
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
    return response.json()


def index_json(json_data: dict, tenant_id: str = "default", declaration_id: str | None = None):
    """Index a declaration from JSON.
    
    Args:
        json_data: JSON data of the declaration
        tenant_id: Tenant identifier
        declaration_id: Optional declaration ID
    """
    response = requests.post(
        f"{API_BASE_URL}/index",
        json={
            "declaration_id": declaration_id,
            "tenant_id": tenant_id,
            "json_data": json_data
        }
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
    return response.json()


def index_ocr(ocr_text: str, tenant_id: str = "default", declaration_id: str | None = None):
    """Index a declaration from OCR text.
    
    Args:
        ocr_text: OCR text content
        tenant_id: Tenant identifier
        declaration_id: Optional declaration ID
    """
    response = requests.post(
        f"{API_BASE_URL}/index",
        json={
            "declaration_id": declaration_id,
            "tenant_id": tenant_id,
            "ocr_text": ocr_text
        }
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
    return response.json()


def index_file(file_path: Path, tenant_id: str = "default"):
    """Index a declaration from file (XML or JSON).
    
    Args:
        file_path: Path to the file
        tenant_id: Tenant identifier
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if file_path.suffix == ".xml":
        return index_xml(content, tenant_id)
    elif file_path.suffix == ".json":
        json_data = json.loads(content)
        return index_json(json_data, tenant_id)
    else:
        print(f"Unsupported file format: {file_path.suffix}")
        return None


if __name__ == "__main__":
    # Example 1: Index from XML file
    print("Example 1: Index from XML file")
    xml_file = Path("examples/data/sample_declaration.xml")
    if xml_file.exists():
        result = index_file(xml_file)
        if result:
            print(f"✓ Indexed declaration: {result['declaration_id']}")
            print(f"  Chunks: {result['chunks_count']}")
            print(f"  Status: {result['status']}")
    
    # Example 2: Index from JSON file
    print("\n\nExample 2: Index from JSON file")
    json_file = Path("examples/data/sample_declaration.json")
    if json_file.exists():
        result = index_file(json_file)
        if result:
            print(f"✓ Indexed declaration: {result['declaration_id']}")
            print(f"  Chunks: {result['chunks_count']}")
    
    # Example 3: Index from OCR text
    print("\n\nExample 3: Index from OCR text")
    ocr_text = """
    Номер декларации: DT-2023-005678
    Дата выпуска: 20.07.2023
    Производитель: Apple Inc.
    Код товара: 8517120000
    Описание: Смартфоны iPhone 14 Pro, объем памяти 512 ГБ
    Страна происхождения: CN
    Таможенная стоимость: 2000000 USD
    """
    result = index_ocr(ocr_text)
    if result:
        print(f"✓ Indexed declaration: {result['declaration_id']}")
        print(f"  Chunks: {result['chunks_count']}")
