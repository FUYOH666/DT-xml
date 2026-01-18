"""Семантическое чанкование деклараций."""

import logging
import uuid
from typing import Any

from dt_xml.chunker.section_extractor import SectionExtractor
from dt_xml.config.models import DeclarationChunk
from dt_xml.config.settings import get_settings

logger = logging.getLogger(__name__)


class SemanticChunker:
    """Семантическое чанкование документов с сохранением контекста."""

    def __init__(self):
        """Инициализация чанкера."""
        self.settings = get_settings()
        self.section_extractor = SectionExtractor()
        self.chunk_size = self.settings.chunking.chunk_size
        self.chunk_overlap = self.settings.chunking.chunk_overlap
        self.min_chunk_size = self.settings.chunking.min_chunk_size
        self.preserve_structure = self.settings.chunking.preserve_structure

    def chunk_declaration(
        self,
        declaration_id: str,
        text: str,
        data: dict[str, Any] | None = None,
    ) -> list[DeclarationChunk]:
        """Разбиение декларации на чанки.

        Args:
            declaration_id: Идентификатор декларации.
            text: Текст декларации.
            data: Структурированные данные декларации.

        Returns:
            Список чанков декларации.
        """
        chunks: list[DeclarationChunk] = []

        if self.preserve_structure:
            # Чанкование с сохранением структуры секций
            chunks = self._chunk_by_sections(declaration_id, text, data)
        else:
            # Простое чанкование по размеру
            chunks = self._chunk_by_size(declaration_id, text, data)

        return chunks

    def _chunk_by_sections(
        self,
        declaration_id: str,
        text: str,
        data: dict[str, Any] | None = None,
    ) -> list[DeclarationChunk]:
        """Чанкование по секциям с сохранением структуры.

        Args:
            declaration_id: Идентификатор декларации.
            text: Текст декларации.
            data: Структурированные данные.

        Returns:
            Список чанков.
        """
        chunks: list[DeclarationChunk] = []

        # Извлечение секций
        sections = self.section_extractor.extract_sections(text, data)

        chunk_index = 0
        for section in sections:
            section_name = section["section"]
            section_content = section["content"]
            section_metadata = section.get("metadata", {})

            # Если секция слишком большая, разбиваем её на подчанки
            if len(section_content) > self.chunk_size:
                sub_chunks = self._split_large_section(
                    section_content,
                    section_name,
                    section_metadata,
                )
                for sub_chunk_content in sub_chunks:
                    chunk = DeclarationChunk(
                        chunk_id=str(uuid.uuid4()),
                        declaration_id=declaration_id,
                        content=sub_chunk_content,
                        section=section_name,
                        chunk_index=chunk_index,
                        metadata={
                            **section_metadata,
                            "section": section_name,
                            "preserve_structure": True,
                        },
                    )
                    chunks.append(chunk)
                    chunk_index += 1
            else:
                # Секция помещается в один чанк
                if len(section_content) >= self.min_chunk_size:
                    chunk = DeclarationChunk(
                        chunk_id=str(uuid.uuid4()),
                        declaration_id=declaration_id,
                        content=section_content,
                        section=section_name,
                        chunk_index=chunk_index,
                        metadata={
                            **section_metadata,
                            "section": section_name,
                            "preserve_structure": True,
                        },
                    )
                    chunks.append(chunk)
                    chunk_index += 1

        return chunks

    def _chunk_by_size(
        self,
        declaration_id: str,
        text: str,
        data: dict[str, Any] | None = None,
    ) -> list[DeclarationChunk]:
        """Простое чанкование по размеру с перекрытием.

        Args:
            declaration_id: Идентификатор декларации.
            text: Текст декларации.
            data: Структурированные данные (не используются в этом методе).

        Returns:
            Список чанков.
        """
        chunks: list[DeclarationChunk] = []

        if not text or len(text) < self.min_chunk_size:
            # Если текст слишком короткий, создаем один чанк
            if text:
                chunk = DeclarationChunk(
                    chunk_id=str(uuid.uuid4()),
                    declaration_id=declaration_id,
                    content=text,
                    section=None,
                    chunk_index=0,
                    metadata={"preserve_structure": False},
                )
                chunks.append(chunk)
            return chunks

        # Разбиение текста на слова/токены
        words = text.split()
        current_chunk_words: list[str] = []
        chunk_index = 0

        for word in words:
            current_chunk_words.append(word)
            current_chunk_text = " ".join(current_chunk_words)

            # Если достигли размера чанка
            if len(current_chunk_text) >= self.chunk_size:
                chunk = DeclarationChunk(
                    chunk_id=str(uuid.uuid4()),
                    declaration_id=declaration_id,
                    content=current_chunk_text,
                    section=None,
                    chunk_index=chunk_index,
                    metadata={"preserve_structure": False},
                )
                chunks.append(chunk)
                chunk_index += 1

                # Сохраняем перекрытие
                if self.chunk_overlap > 0:
                    overlap_words = current_chunk_words[-self.chunk_overlap :]
                    current_chunk_words = overlap_words
                else:
                    current_chunk_words = []

        # Добавляем последний чанк, если есть остаток
        if current_chunk_words:
            remaining_text = " ".join(current_chunk_words)
            if len(remaining_text) >= self.min_chunk_size:
                chunk = DeclarationChunk(
                    chunk_id=str(uuid.uuid4()),
                    declaration_id=declaration_id,
                    content=remaining_text,
                    section=None,
                    chunk_index=chunk_index,
                    metadata={"preserve_structure": False},
                )
                chunks.append(chunk)

        return chunks

    def _split_large_section(
        self,
        content: str,
        section_name: str,
        metadata: dict[str, Any],
    ) -> list[str]:
        """Разбиение большой секции на подчанки.

        Args:
            content: Содержимое секции.
            section_name: Название секции.
            metadata: Метаданные секции.

        Returns:
            Список подчанков.
        """
        sub_chunks: list[str] = []

        # Разбиение по предложениям, если возможно
        sentences = content.split(". ")
        current_chunk_sentences: list[str] = []

        for sentence in sentences:
            current_chunk_sentences.append(sentence)
            current_chunk_text = ". ".join(current_chunk_sentences)

            if len(current_chunk_text) >= self.chunk_size:
                sub_chunks.append(current_chunk_text)

                # Сохраняем перекрытие
                if self.chunk_overlap > 0:
                    overlap_sentences = current_chunk_sentences[-self.chunk_overlap :]
                    current_chunk_sentences = overlap_sentences
                else:
                    current_chunk_sentences = []

        # Добавляем последний подчанк
        if current_chunk_sentences:
            remaining_text = ". ".join(current_chunk_sentences)
            if len(remaining_text) >= self.min_chunk_size:
                sub_chunks.append(remaining_text)

        return sub_chunks if sub_chunks else [content]
