"""Модуль обработки OCR результатов."""

from dt_xml.ocr.field_extractor import FieldExtractor
from dt_xml.ocr.ocr_normalizer import OCRNormalizer
from dt_xml.ocr.ocr_processor import OCRProcessor

__all__ = ["OCRProcessor", "FieldExtractor", "OCRNormalizer"]
