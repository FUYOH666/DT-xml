"""Эндпоинт поиска."""

import time

from fastapi import APIRouter, HTTPException

from dt_xml.api.schemas.response import SearchResponse, SearchResultResponse
from dt_xml.api.schemas.search import SearchRequest
from dt_xml.reranker.explainability import Explainability
from dt_xml.search.hybrid_search import HybridSearch
from dt_xml.temporal.temporal_awareness import TemporalAwareness

router = APIRouter(prefix="/search", tags=["search"])

# Инициализация компонентов
hybrid_search = HybridSearch()
temporal_awareness = TemporalAwareness()
explainability = Explainability()


@router.post("/", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """Поиск по декларациям."""
    start_time = time.time()

    try:
        # Гибридный поиск
        results = hybrid_search.search(
            query=request.query,
            top_k=request.top_k,
            filters=request.filters,
        )

        # Реранкинг, если включен
        if request.rerank and results:
            from dt_xml.reranker.adaptive_reranker import AdaptiveReranker

            reranker = AdaptiveReranker()
            documents = [r.get("content", "") for r in results]
            reranked = reranker.rerank(request.query, documents, top_k=request.top_k)

            # Обновление результатов с новыми скорами
            for i, rerank_result in enumerate(reranked):
                if i < len(results):
                    results[i]["score"] = rerank_result["score"]
                    results[i]["rerank_info"] = {
                        "complexity": rerank_result.get("complexity"),
                        "model_used": rerank_result.get("model_used"),
                    }

        # Применение временной осведомленности
        for result in results:
            result = temporal_awareness.add_temporal_context(result)
            if "date_issued" in request.filters:
                # Корректировка скора с учетом даты
                result["score"] = temporal_awareness.adjust_score_by_date(
                    result,
                    request.filters.get("date_issued"),
                )

        # Добавление объяснений, если запрошено
        if request.explain:
            for result in results:
                explanation = explainability.explain(request.query, result)
                result["explanation"] = explanation
                result["matched_fields"] = explanation.get("matched_fields", [])

        # Преобразование в формат ответа
        search_results = [
            SearchResultResponse(
                declaration_id=result.get("declaration_id", ""),
                chunk_id=result.get("chunk_id"),
                content=result.get("content", ""),
                score=result.get("score", 0.0),
                metadata=result.get("metadata", {}),
                explanation=result.get("explanation"),
                matched_fields=result.get("matched_fields", []),
            )
            for result in results
        ]

        query_time_ms = (time.time() - start_time) * 1000

        return SearchResponse(
            results=search_results,
            total=len(search_results),
            query_time_ms=query_time_ms,
            query=request.query,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при поиске: {str(e)}")
