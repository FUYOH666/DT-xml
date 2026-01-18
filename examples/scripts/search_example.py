#!/usr/bin/env python3
"""Example script for searching declarations."""

import requests
import json
from datetime import datetime, timedelta

API_BASE_URL = "http://localhost:8000"


def search_declarations(query: str, filters: dict | None = None, top_k: int = 10):
    """Search for declarations.
    
    Args:
        query: Search query text
        filters: Optional filters (manufacturer, date_issued, etc.)
        top_k: Number of results to return
    """
    response = requests.post(
        f"{API_BASE_URL}/search",
        json={
            "query": query,
            "tenant_id": "default",
            "top_k": top_k,
            "filters": filters or {},
            "explain": True
        }
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
    return response.json()


def print_results(results: dict):
    """Print search results in a readable format."""
    if not results:
        return
    
    print(f"\nFound {results['total']} results (query time: {results['query_time_ms']:.2f}ms)")
    print("=" * 80)
    
    for i, result in enumerate(results["results"], 1):
        print(f"\n{i}. Declaration: {result['declaration_id']}")
        print(f"   Score: {result['score']:.4f}")
        print(f"   Content: {result['content'][:150]}...")
        
        metadata = result.get("metadata", {})
        if metadata:
            print(f"   Manufacturer: {metadata.get('manufacturer', 'N/A')}")
            print(f"   Date: {metadata.get('date_issued', 'N/A')}")
            print(f"   Product Code: {metadata.get('product_code', 'N/A')}")
        
        explanation = result.get("explanation")
        if explanation:
            print(f"   Matched fields: {', '.join(explanation.get('matched_fields', []))}")
            if explanation.get("reasons"):
                print(f"   Reasons: {'; '.join(explanation['reasons'][:2])}")


if __name__ == "__main__":
    # Example 1: Search by manufacturer
    print("Example 1: Search for Samsung declarations")
    results = search_declarations(
        "Samsung smartphones",
        filters={
            "manufacturer": "Samsung",
            "date_issued": {"gte": "2023-01-01", "lte": "2023-12-31"}
        }
    )
    print_results(results)
    
    # Example 2: Search by HS code
    print("\n\nExample 2: Search by HS code 8517120000")
    results = search_declarations(
        "8517120000",
        filters={"product_code": "8517120000"}
    )
    print_results(results)
    
    # Example 3: Semantic search
    print("\n\nExample 3: Semantic search for mobile phones")
    results = search_declarations(
        "мобильные телефоны с большим экраном",
        top_k=5
    )
    print_results(results)
