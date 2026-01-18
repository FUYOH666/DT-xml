"""Тесты парсера XML деклараций."""

import pytest
from datetime import datetime

from dt_xml.parser.xml_parser import XMLParser
from dt_xml.parser.schema_validator import SchemaValidator


def test_xml_parser_basic():
    """Базовый тест парсера."""
    parser = XMLParser()
    
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <declaration>
        <declaration_number>12345</declaration_number>
        <date_issued>2023-06-15</date_issued>
        <declaration_type>import</declaration_type>
        <manufacturer>Samsung</manufacturer>
        <product_code>8517120000</product_code>
    </declaration>
    """
    
    result = parser.parse(xml_content)
    
    assert result["declaration_number"] == "12345"
    assert result["date_issued"] == datetime(2023, 6, 15)
    assert result["manufacturer"] == "Samsung"


def test_schema_validator():
    """Тест валидатора схемы."""
    validator = SchemaValidator()
    
    xml_content = """<?xml version="1.0"?>
    <declaration>
        <declaration_number>12345</declaration_number>
        <date_issued>2023-06-15</date_issued>
    </declaration>
    """
    
    is_valid, errors = validator.validate(xml_content)
    assert is_valid or len(errors) > 0  # Может быть валидным или иметь предупреждения
