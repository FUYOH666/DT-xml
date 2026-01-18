"""Эндпоинт управления схемами заказчиков."""

from typing import Any

from fastapi import APIRouter, HTTPException

from dt_xml.api.schemas.search import SchemaRegistrationRequest
from dt_xml.schema.schema_manager import SchemaManager

router = APIRouter(prefix="/schema", tags=["schema"])

# Инициализация менеджера схем
schema_manager = SchemaManager()


@router.post("/register")
async def register_schema(request: SchemaRegistrationRequest) -> dict[str, str]:
    """Регистрация схемы заказчика."""
    try:
        # Формирование полной конфигурации схемы
        schema_config = {
            "tenant_id": request.tenant_id,
            "tenant_name": request.tenant_name,
            "schema": request.schema,
            "processing": request.processing,
            "search": request.search,
        }

        # Регистрация схемы
        schema_manager.register_tenant_schema(request.tenant_id, schema_config)

        return {
            "status": "success",
            "message": f"Схема для заказчика {request.tenant_id} успешно зарегистрирована",
            "tenant_id": request.tenant_id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при регистрации схемы: {str(e)}")


@router.get("/{tenant_id}")
async def get_schema(tenant_id: str) -> dict[str, Any]:
    """Получение схемы заказчика."""
    try:
        schema_config = schema_manager.registry.get_schema(tenant_id)

        if schema_config is None:
            raise HTTPException(status_code=404, detail=f"Схема для заказчика {tenant_id} не найдена")

        return schema_config

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении схемы: {str(e)}")


@router.get("/")
async def list_schemas() -> dict[str, list[str]]:
    """Получение списка всех зарегистрированных схем."""
    try:
        tenants = schema_manager.registry.list_tenants()
        return {"tenants": tenants, "count": len(tenants)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении списка схем: {str(e)}")
