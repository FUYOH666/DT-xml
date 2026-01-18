"""Хранилище метаданных деклараций в PostgreSQL."""

import logging
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Column, DateTime, String, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from dt_xml.config.models import DeclarationMetadata
from dt_xml.config.settings import get_settings

logger = logging.getLogger(__name__)

Base = declarative_base()


class DeclarationMetadataModel(Base):
    """Модель метаданных декларации в БД."""

    __tablename__ = "declaration_metadata"

    declaration_id = Column(String, primary_key=True)
    declaration_number = Column(String, nullable=False, index=True)
    date_issued = Column(DateTime, nullable=False, index=True)
    declaration_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    manufacturer = Column(String, index=True)
    importer = Column(String, index=True)
    exporter = Column(String, index=True)
    product_code = Column(String, index=True)
    country_origin = Column(String, index=True)
    customs_value = Column(String)
    currency = Column(String)
    quantity = Column(String)
    unit_of_measure = Column(String)
    language = Column(String)
    version = Column(String)
    source = Column(String)
    processed_at = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column(JSON)  # Дополнительные метаданные


class MetadataStore:
    """Хранилище метаданных деклараций."""

    def __init__(self):
        """Инициализация хранилища метаданных."""
        self.settings = get_settings()
        self.engine = create_engine(
            self.settings.database.url,
            pool_size=self.settings.database.pool_size,
            max_overflow=self.settings.database.max_overflow,
        )
        self.SessionLocal = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self) -> None:
        """Создание таблиц в БД."""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Таблицы метаданных созданы/проверены")
        except Exception as e:
            logger.error(f"Ошибка при создании таблиц: {e}")
            raise

    def save_metadata(self, metadata: DeclarationMetadata, declaration_id: str | None = None) -> str:
        """Сохранение метаданных декларации.

        Args:
            metadata: Метаданные декларации.
            declaration_id: Идентификатор декларации. Если None, генерируется из номера.

        Returns:
            Идентификатор декларации.
        """
        if declaration_id is None:
            declaration_id = metadata.declaration_number

        session = self.SessionLocal()
        try:
            # Проверка существования
            existing = session.query(DeclarationMetadataModel).filter_by(
                declaration_id=declaration_id
            ).first()

            db_metadata = DeclarationMetadataModel(
                declaration_id=declaration_id,
                declaration_number=metadata.declaration_number,
                date_issued=metadata.date_issued,
                declaration_type=metadata.declaration_type.value,
                status=metadata.status.value,
                manufacturer=metadata.manufacturer,
                importer=metadata.importer,
                exporter=metadata.exporter,
                product_code=metadata.product_code,
                country_origin=metadata.country_origin,
                customs_value=str(metadata.customs_value) if metadata.customs_value else None,
                currency=metadata.currency,
                quantity=str(metadata.quantity) if metadata.quantity else None,
                unit_of_measure=metadata.unit_of_measure,
                language=metadata.language,
                version=metadata.version,
                source=metadata.source,
                processed_at=metadata.processed_at or datetime.utcnow(),
                metadata_json=metadata.model_dump(),
            )

            if existing:
                # Обновление существующей записи
                for key, value in db_metadata.__dict__.items():
                    if key != "declaration_id":
                        setattr(existing, key, value)
                session.commit()
                logger.info(f"Метаданные декларации {declaration_id} обновлены")
            else:
                # Создание новой записи
                session.add(db_metadata)
                session.commit()
                logger.info(f"Метаданные декларации {declaration_id} сохранены")

            return declaration_id

        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка при сохранении метаданных: {e}")
            raise
        finally:
            session.close()

    def get_metadata(self, declaration_id: str) -> DeclarationMetadata | None:
        """Получение метаданных декларации.

        Args:
            declaration_id: Идентификатор декларации.

        Returns:
            Метаданные декларации или None.
        """
        session = self.SessionLocal()
        try:
            db_metadata = session.query(DeclarationMetadataModel).filter_by(
                declaration_id=declaration_id
            ).first()

            if db_metadata:
                # Восстановление из JSON, если доступно
                if db_metadata.metadata_json:
                    return DeclarationMetadata(**db_metadata.metadata_json)
                else:
                    # Создание из полей БД
                    return DeclarationMetadata(
                        declaration_number=db_metadata.declaration_number,
                        date_issued=db_metadata.date_issued,
                        declaration_type=db_metadata.declaration_type,
                        status=db_metadata.status,
                        manufacturer=db_metadata.manufacturer,
                        importer=db_metadata.importer,
                        exporter=db_metadata.exporter,
                        product_code=db_metadata.product_code,
                        country_origin=db_metadata.country_origin,
                        customs_value=float(db_metadata.customs_value) if db_metadata.customs_value else None,
                        currency=db_metadata.currency,
                        quantity=float(db_metadata.quantity) if db_metadata.quantity else None,
                        unit_of_measure=db_metadata.unit_of_measure,
                        language=db_metadata.language,
                        version=db_metadata.version,
                        source=db_metadata.source,
                        processed_at=db_metadata.processed_at,
                    )

            return None

        except Exception as e:
            logger.error(f"Ошибка при получении метаданных: {e}")
            return None
        finally:
            session.close()

    def search_by_filters(self, filters: dict[str, Any], limit: int = 100) -> list[DeclarationMetadata]:
        """Поиск метаданных по фильтрам.

        Args:
            filters: Словарь фильтров (поле -> значение).
            limit: Максимальное количество результатов.

        Returns:
            Список метаданных деклараций.
        """
        session = self.SessionLocal()
        try:
            query = session.query(DeclarationMetadataModel)

            # Применение фильтров
            if "manufacturer" in filters:
                query = query.filter(DeclarationMetadataModel.manufacturer == filters["manufacturer"])
            if "importer" in filters:
                query = query.filter(DeclarationMetadataModel.importer == filters["importer"])
            if "product_code" in filters:
                query = query.filter(DeclarationMetadataModel.product_code == filters["product_code"])
            if "country_origin" in filters:
                query = query.filter(DeclarationMetadataModel.country_origin == filters["country_origin"])
            if "date_issued_from" in filters:
                query = query.filter(DeclarationMetadataModel.date_issued >= filters["date_issued_from"])
            if "date_issued_to" in filters:
                query = query.filter(DeclarationMetadataModel.date_issued <= filters["date_issued_to"])

            results = query.limit(limit).all()

            metadata_list = []
            for db_metadata in results:
                if db_metadata.metadata_json:
                    metadata_list.append(DeclarationMetadata(**db_metadata.metadata_json))
                else:
                    metadata_list.append(
                        DeclarationMetadata(
                            declaration_number=db_metadata.declaration_number,
                            date_issued=db_metadata.date_issued,
                            declaration_type=db_metadata.declaration_type,
                            status=db_metadata.status,
                            manufacturer=db_metadata.manufacturer,
                            importer=db_metadata.importer,
                            exporter=db_metadata.exporter,
                            product_code=db_metadata.product_code,
                            country_origin=db_metadata.country_origin,
                            customs_value=float(db_metadata.customs_value) if db_metadata.customs_value else None,
                            currency=db_metadata.currency,
                            quantity=float(db_metadata.quantity) if db_metadata.quantity else None,
                            unit_of_measure=db_metadata.unit_of_measure,
                            language=db_metadata.language,
                            version=db_metadata.version,
                            source=db_metadata.source,
                            processed_at=db_metadata.processed_at,
                        )
                    )

            return metadata_list

        except Exception as e:
            logger.error(f"Ошибка при поиске метаданных: {e}")
            return []
        finally:
            session.close()

    def delete_metadata(self, declaration_id: str) -> None:
        """Удаление метаданных декларации.

        Args:
            declaration_id: Идентификатор декларации.
        """
        session = self.SessionLocal()
        try:
            db_metadata = session.query(DeclarationMetadataModel).filter_by(
                declaration_id=declaration_id
            ).first()

            if db_metadata:
                session.delete(db_metadata)
                session.commit()
                logger.info(f"Метаданные декларации {declaration_id} удалены")
            else:
                logger.warning(f"Метаданные декларации {declaration_id} не найдены")

        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка при удалении метаданных: {e}")
            raise
        finally:
            session.close()
