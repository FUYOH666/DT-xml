#!/usr/bin/env python3
"""Скрипт загрузки и индексации деклараций."""

import argparse
import logging
from pathlib import Path

from dt_xml.chunker.semantic_chunker import SemanticChunker
from dt_xml.embedding.multilingual_embedder import MultilingualEmbedder
from dt_xml.normalizer.field_normalizer import FieldNormalizer
from dt_xml.parser.xml_parser import XMLParser
from dt_xml.storage.document_store import DocumentStore
from dt_xml.storage.metadata_store import MetadataStore
from dt_xml.storage.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Основная функция."""
    parser = argparse.ArgumentParser(description="Загрузка и индексация деклараций")
    parser.add_argument("--input", type=str, required=True, help="Путь к XML файлу или директории")
    parser.add_argument("--batch-size", type=int, default=10, help="Размер батча для обработки")

    args = parser.parse_args()

    input_path = Path(args.input)

    # Инициализация компонентов
    xml_parser = XMLParser()
    normalizer = FieldNormalizer()
    chunker = SemanticChunker()
    embedder = MultilingualEmbedder()
    vector_store = VectorStore()
    metadata_store = MetadataStore()
    document_store = DocumentStore()

    # Обработка файлов
    if input_path.is_file():
        files = [input_path]
    elif input_path.is_dir():
        files = list(input_path.glob("*.xml"))
    else:
        logger.error(f"Путь не существует: {input_path}")
        return

    logger.info(f"Найдено {len(files)} файлов для обработки")

    # Обработка батчами
    for i in range(0, len(files), args.batch_size):
        batch_files = files[i : i + args.batch_size]
        logger.info(f"Обработка батча {i//args.batch_size + 1}: {len(batch_files)} файлов")

        for file_path in batch_files:
            try:
                # Парсинг
                parsed_data = xml_parser.parse_file(file_path)

                # Нормализация
                normalized_data = normalizer.normalize_all_fields(parsed_data)

                # Получение идентификатора
                declaration_id = normalized_data.get("declaration_number", file_path.stem)

                # Получение текста
                text = normalized_data.get("full_text", "") or normalized_data.get("product_description", "")

                # Чанкование
                chunks = chunker.chunk_declaration(declaration_id, text, normalized_data)

                # Генерация эмбедингов
                chunk_texts = [chunk.content for chunk in chunks]
                embeddings = embedder.embed_batch(chunk_texts)

                # Сохранение
                vector_store.add_chunks(chunks, embeddings)
                metadata = xml_parser.to_metadata(normalized_data)
                metadata_store.save_metadata(metadata, declaration_id)
                document_store.save_document(declaration_id, normalized_data, metadata.model_dump())

                logger.info(f"Декларация {declaration_id} проиндексирована ({len(chunks)} чанков)")

            except Exception as e:
                logger.error(f"Ошибка при обработке {file_path}: {e}")

    logger.info("Индексация завершена")


if __name__ == "__main__":
    main()
