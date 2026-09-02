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
    def extract_page_text(page) -> str:
        """
        Extrae el texto de una página individual.
        """
        return page.get_text("text").strip()

    @staticmethod
    def render_page(page) -> bytes:
        """
        Convierte una página a JPEG optimizado para visión.
        """
        pixmap = page.get_pixmap(
            matrix=pymupdf.Matrix(1.25, 1.25),
            alpha=False
        )

        image_data = pixmap.tobytes(
            "jpeg",
            jpg_quality=90
        )

        print(
            f"Page {page.number + 1}: "
            f"{len(image_data) / 1024:.1f} KB"
        )

        return image_data

    @classmethod
    def get_resume_content(
        cls,
        file_id: str
    ) -> dict:

        pdf_data = cls.get_file(file_id)

        document = pymupdf.open(
            stream=pdf_data,
            filetype="pdf"
        )

        pages = []

        total_text_length = 0
        image_pages = 0

        for page in document:

            text = cls.extract_page_text(page)

            if len(text) >= cls.MIN_TEXT_LENGTH:
                pages.append({
                    "page": page.number + 1,
                    "type": "text",
                    "content": text
                })

                total_text_length += len(text)

            else:
                image_data = cls.render_page(page)

                pages.append({
                    "page": page.number + 1,
                    "type": "image",
                    "content": image_data
                })

                image_pages += 1

        document.close()

        # Si todas las páginas tienen texto,
        # mantenemos exactamente el flujo anterior.
        if image_pages == 0:

            text = "\n\n".join(
                page["content"]
                for page in pages
            )

            return {
                "type": "text",
                "content": text
            }

        # Si ninguna página tiene texto,
        # mantenemos el flujo anterior de imágenes.
        if total_text_length == 0:

            images = [
                page["content"]
                for page in pages
            ]

            return {
                "type": "images",
                "content": images
            }

        # Documento híbrido:
        # algunas páginas contienen texto
        # y otras necesitan visión.
        return {
            "type": "hybrid",
            "content": pages
        }

    @classmethod
    def get_resume_images(
        cls,
        file_id: str
    ) -> list[bytes]:

        pdf_data = cls.get_file(file_id)

        document = pymupdf.open(
            stream=pdf_data,
            filetype="pdf"
        )

        images = []

        for page in document:

            image_data = cls.render_page(page)

            images.append(image_data)

        document.close()

        return images