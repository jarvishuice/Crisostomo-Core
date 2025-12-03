import pytest
import os
from Application.Helpers.Pdf.PDFPreviewHelper import PDFPreviewHelper

@pytest.fixture
def helper():
    return PDFPreviewHelper()

def test_generate_preview_creates_file(helper, tmp_path):
    """
    Testea que generate_preview genera un archivo PNG a partir de un PDF.
    tmp_path es un directorio temporal que pytest crea automáticamente.
    """
    input_pdf = "./media/pdf/02cea2c7d63b4021baa78dee91f62280.pdf"
    output_png = tmp_path / "de.png"

    # Ejecutamos la generación
    helper.generate_preview(input_pdf, str(output_png))

    # Verificamos que el archivo fue creado
    assert os.path.exists(output_png)
    # Opcional: verificamos que el archivo no esté vacío
    print(os.path.getsize(output_png))
    assert os.path.getsize(output_png) > 0
