from pathlib import Path

import fitz
from docx import Document as DocxDocument
from easyocr import Reader
from lingua import Language, LanguageDetectorBuilder


class DocumentProcessor:
    def __init__(self):
        self.ocr_reader = Reader(["en"], gpu=False)

        self.language_detector = (
            LanguageDetectorBuilder
            .from_languages(
                Language.ENGLISH,
                Language.GERMAN,
                Language.FRENCH,
                Language.SPANISH,
            )
            .build()
        )

    async def extract_text(self, file_path: str) -> str:
        path = Path(file_path)

        suffix = path.suffix.lower()

        if suffix == ".txt":
            return path.read_text(errors="ignore")

        elif suffix == ".pdf":
            return self.extract_pdf_text(file_path)

        elif suffix == ".docx":
            return self.extract_docx_text(file_path)

        elif suffix in [".png", ".jpg", ".jpeg"]:
            return self.extract_image_text(file_path)

        return ""

    def extract_pdf_text(self, file_path: str) -> str:
        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        return text

    def extract_docx_text(self, file_path: str) -> str:
        document = DocxDocument(file_path)

        return "\n".join(
            [paragraph.text for paragraph in document.paragraphs]
        )

    def extract_image_text(self, file_path: str) -> str:
        results = self.ocr_reader.readtext(file_path)

        return "\n".join([result[1] for result in results])

    def detect_language(self, text: str) -> str:
        detected = self.language_detector.detect_language_of(text)

        if not detected:
            return "unknown"

        return detected.iso_code_639_1.name.lower()