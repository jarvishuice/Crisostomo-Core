import os
from pdf2image import convert_from_path
from PIL import Image

class PDFPreviewHelper:

    def __init__(self):
        """
        poppler_path: ruta donde está el binario de poppler (solo Windows)
        """
        self.poppler_path = "./Utils/poppler/Library/bin"

    def generate_preview(self, pdf_path: str, output_path: str) -> str:
        """
        Lee un PDF y extrae una previsualización PNG de la primera página.

        pdf_path: ruta completa al PDF
        output_path: ruta completa donde guardar el PNG (incluye el nombre del archivo)

        Retorna: la ruta donde se guardó el PNG
        """
        try:
            # Convertir solo la primera página
            images = convert_from_path(
                pdf_path,
                first_page=1,
                last_page=1,
                poppler_path=self.poppler_path
            )

            if not images:
                raise Exception("No se pudo leer la primera página del PDF.")

            # Tomar primera imagen
            img: Image.Image = images[0]

            # Crear carpeta si no existe
            folder = os.path.dirname(output_path)
            os.makedirs(folder, exist_ok=True)

            # Guardar como PNG
            img.save(output_path, "PNG")

            return output_path

        except Exception as e:
            raise Exception(f"Error generando imagen de previsualización: {e}")


