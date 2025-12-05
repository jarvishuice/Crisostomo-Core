import io
import json
import os
from logging import getLogger

from PIL import Image
from fastapi import APIRouter, Response, status, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse

from Config.Settings import Settings
from Domain.Entities.Book.BookEntity import BookEntity
from Infrastructure.DAO.Book.BookDAO import BookDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster

from Presentation.Services.BookService import BookService

BOOK_ROUTER = APIRouter(
    prefix="/book",
    tags=["book"],

)
settings = Settings()


def get_dao():
    pool = PostgreSQLPoolMaster.get_instance()
    return BookDAO(pool)


log = getLogger("AppLogger")


@BOOK_ROUTER.post("/", status_code=status.HTTP_200_OK)
async def create(book: str = Form(...), pdf_file: UploadFile = File(...), dao: BookDAO = Depends(get_dao)) -> Response:
    services = BookService(dao)
    try:
        book_data = json.loads(book)
        book_entity = BookEntity(**book_data)
        res = await services.save(book_entity, pdf_file)
        if not res:
            raise

        return Response(status_code=status.HTTP_201_CREATED,
                        media_type="application/json")
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )


@BOOK_ROUTER.get("/", status_code=status.HTTP_200_OK)
async def get(size: int = 100, page: int = 1, dao: BookDAO = Depends(get_dao)) -> Response:
    services = BookService(dao)
    try:
        res = await services.get_books(size, page)

        return Response(status_code=status.HTTP_200_OK,
                        media_type="application/json",
                        content=json.dumps([u.serialize() for u in res]))
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )


@BOOK_ROUTER.get("/filter/category/{category}", status_code=status.HTTP_200_OK)
async def filterByCategory(category: str, dao: BookDAO = Depends(get_dao)) -> Response:
    services = BookService(dao)
    try:
        res = await services.getByCategory(category)

        return Response(status_code=status.HTTP_200_OK,
                        media_type="application/json",
                        content=json.dumps([u.serialize() for u in res]))
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )


@BOOK_ROUTER.get("/filter/area/{area}", status_code=status.HTTP_200_OK)
async def filterByArea(area: str, dao: BookDAO = Depends(get_dao)) -> Response:
    services = BookService(dao)
    try:
        res = await services.getByArea(area)

        return Response(status_code=status.HTTP_200_OK,
                        media_type="application/json",
                        content=json.dumps([u.serialize() for u in res]))
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )


@BOOK_ROUTER.get("/filter/subarea/{subarea}", status_code=status.HTTP_200_OK)
async def filterBySubArea(subArea: str, dao: BookDAO = Depends(get_dao)) -> Response:
    services = BookService(dao)
    try:
        res = await services.getBySubArea(subArea)

        return Response(status_code=status.HTTP_200_OK,
                        media_type="application/json",
                        content=json.dumps([u.serialize() for u in res]))
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )
@BOOK_ROUTER.get("/filter/auhtor/{author}", status_code=status.HTTP_200_OK)
async def filterByAuthor(author: str, dao: BookDAO = Depends(get_dao)) -> Response:
    services = BookService(dao)
    try:
        res = await services.getByAuthor(author)

        return Response(status_code=status.HTTP_200_OK,
                        media_type="application/json",
                        content=json.dumps([u.serialize() for u in res]))
    except Exception as ex:
        raise (HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        ))

@BOOK_ROUTER.get("/filter/user/{user}", status_code=status.HTTP_200_OK)
async def filterByUser(user: str, dao: BookDAO = Depends(get_dao)) -> Response:
    services = BookService(dao)
    try:
        res = await services.getByUser(user)

        return Response(status_code=status.HTTP_200_OK,
                        media_type="application/json",
                        content=json.dumps([u.serialize() for u in res]))
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )
@BOOK_ROUTER.get("/preview-pdf/{code}", status_code=status.HTTP_200_OK)
async def preview_pdf(code: str, dao: BookDAO = Depends(get_dao)):
    """
    Devuelve el PDF para previsualización en el navegador.
    Si el cliente quiere, puede descargarse usando la opción del navegador.
    """
    pdf_path = os.path.join(settings.PDF_PATH, f"{code}.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF no encontrado")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{code}.pdf",
        headers={"Content-Disposition": f"inline; filename={code}.pdf"}
    )

@BOOK_ROUTER.get("/pdf/{code}", status_code=status.HTTP_200_OK)
async def get_pdf(code: str, dao: BookDAO = Depends(get_dao)):
    """
    Devuelve el PDF del libro correspondiente al código.
    """
    pdf_path = os.path.join(settings.PDF_PATH, f"{code}.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF no encontrado")
    return FileResponse(path=pdf_path, media_type="application/pdf", filename=f"{code}.pdf")


@BOOK_ROUTER.get("/img/{cod}/{width}/{height}")
async def get_image(cod: str, width: int = 300, height: int = 300):
    # Ruta de la imagen original
    image_path = os.path.join(settings.BOOK_IMG_PATH, f"{cod}.png")

    if not os.path.exists(image_path):
       image_path = os.path.join(settings.BOOK_IMG_PATH, "default.png")

    try:
        # Abrir imagen original
        image = Image.open(image_path)

        # Redimensionar
        resized_img = image.resize((width, height))

        # Convertir a bytes PNG
        img_bytes = io.BytesIO()
        resized_img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Retornar como StreamingResponse
        return StreamingResponse(img_bytes, media_type="image/png")

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando la imagen: {e}"
        )

