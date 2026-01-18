"""Тесты поиска."""

import pytest
import numpy as np

from dt_xml.search.sparse_search import SparseSearch
from dt_xml.search.dense_search import DenseSearch
from dt_xml.search.hybrid_search import HybridSearch


def test_sparse_search():
    """Тест BM25 поиска."""
    search = SparseSearch()
    
    documents = [
        "Производитель Samsung, товар телефоны",
        "Производитель Apple, товар телефоны",
        "Производитель Samsung, товар планшеты",
    ]
    
    search.index_documents(documents)
    results = search.search("Samsung телефоны", top_k=2)
    
    assert len(results) > 0
    assert results[0]["score"] > 0


def test_hybrid_search():
    """Тест гибридного поиска."""
    search = HybridSearch()
    
    # Тест требует настроенной векторной БД, поэтому может быть пропущен в unit тестах
    pytest.skip("Требует настроенной векторной БД")
