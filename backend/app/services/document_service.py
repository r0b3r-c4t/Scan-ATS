import pymupdf
from bson import ObjectId

from app.database.mongodb import grid_fs


class DocumentService:

    MIN_TEXT_LENGTH = 100

    @staticmethod
    def get_file(file_id: str) -> bytes:
        file = grid_fs.get(ObjectId(file_id))

        return file.read()

    @staticmethod
    def extract_pdf_text(pdf_data: bytes) -> str:
        document = pymupdf.open(
            stream=pdf_data,
            filetype="pdf"
        )

        text_parts = []

        for page in document:
            text = page.get_text("text").strip()

            if text:
                text_parts.append(text)

        document.close()

        return "\n\n".join(text_parts)

    @staticmethod
    def pdf_to_images(pdf_data: bytes) -> list[bytes]:
        document = pymupdf.open(
            stream=pdf_data,
            filetype="pdf"
        )

        images = []

        for page in document:
            pixmap = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2),
                alpha=False
            )

            images.append(
                pixmap.tobytes("png")
            )

        document.close()

        return images

    @classmethod
    def get_resume_content(
        cls,
        file_id: str
    ) -> dict:

        pdf_data = cls.get_file(file_id)

        text = cls.extract_pdf_text(pdf_data)

        if len(text.strip()) >= cls.MIN_TEXT_LENGTH:
            return {
                "type": "text",
                "content": text
            }

        images = cls.pdf_to_images(pdf_data)

        return {
            "type": "images",
            "content": images
        }

    @classmethod
    def get_resume_images(
        cls,
        file_id: str
    ) -> list[bytes]:

        pdf_data = cls.get_file(file_id)

        return cls.pdf_to_images(pdf_data)