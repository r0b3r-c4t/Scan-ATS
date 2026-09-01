import pymupdf
from bson import ObjectId

from app.database.mongodb import grid_fs


class DocumentService:

    @staticmethod
    def get_file(file_id: str) -> bytes:
        file = grid_fs.get(ObjectId(file_id))

        return file.read()

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
    def get_resume_images(
        cls,
        file_id: str
    ) -> list[bytes]:

        pdf_data = cls.get_file(file_id)

        return cls.pdf_to_images(pdf_data)