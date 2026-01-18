"""Основное FastAPI приложение."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dt_xml.api.routes import health, index, schema, search
from dt_xml.config.settings import get_settings

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Создание приложения
app = FastAPI(
    title="DT-XML API",
    description="API для поиска по таможенным декларациям ЕАЭС",
    version="0.1.0",
)

# Настройка CORS
settings = get_settings()
if settings.api.cors_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Подключение роутеров
app.include_router(health.router)
app.include_router(search.router)
app.include_router(index.router)
app.include_router(schema.router)


@app.get("/")
async def root():
    """Корневой эндпоинт."""
    return {
        "name": "DT-XML API",
        "version": "0.1.0",
        "description": "API для поиска по таможенным декларациям ЕАЭС",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "dt_xml.api.main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.api.reload,
    )
