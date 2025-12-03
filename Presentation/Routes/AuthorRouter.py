import io
import json
import os
from logging import getLogger
from fastapi import APIRouter, Response, status, HTTPException, Depends, UploadFile, File
from Domain.IDAO.Author.IAuthorDAO import IAuthorDAO
from Infrastructure.DAO.Author.AuthorDAO import AuthorDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster
from Presentation.DTOS.Authors.AuthorRequest import AuthorRequest
from Presentation.DTOS.Authors.AuthorUpdate import AuthorUpdate
from Presentation.Services.AuthorService import AuthorService
from Config.Settings import Settings
from fastapi.responses import StreamingResponse
from PIL import Image

AUTHOR_ROUTER = APIRouter(
    prefix="/author",
    tags=["author"],

)
se = Settings()
pathIMG = se.AUTHOR_IMG_PATH
os.makedirs(pathIMG, exist_ok=True)

def get_dao():
    pool = PostgreSQLPoolMaster.get_instance()
    return AuthorDAO(pool)


log = getLogger("AppLogger")



@AUTHOR_ROUTER.post("/", status_code=status.HTTP_201_CREATED)
async def create(entity: AuthorRequest, dao: IAuthorDAO = Depends(get_dao)) -> Response:
    services = AuthorService(dao)

    try:
        res = await services.create(entity.name, entity.description)  # faltaba cerrar paréntesis
        if res == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(entity))

        return Response(status_code=status.HTTP_201_CREATED)

    except Exception as ex:
        # Captura cualquier error inesperado
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )

@AUTHOR_ROUTER.get("/", status_code=status.HTTP_200_OK)
async def getAll(dao: AuthorDAO = Depends(get_dao)) -> Response:
    services = AuthorService(dao)
    try:
        res = await services.getAll()
        print(res[0].name)
        return Response(status_code=status.HTTP_200_OK, content=json.dumps([u.serialize() for u in res]),
                        media_type="application/json")
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )


@AUTHOR_ROUTER.get("/{code}", status_code=status.HTTP_200_OK)
async def getOne(code: str, dao: AuthorDAO = Depends(get_dao)) -> Response:
    services = AuthorService(dao)
    log.info("test de router")
    try:
        res = await services.getAuthor(code)

        return Response(status_code=status.HTTP_200_OK, content=json.dumps(res.serialize()),
                        media_type="application/json")
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )


@AUTHOR_ROUTER.get("/search/{param}", status_code=status.HTTP_200_OK)
async def search(param: str, dao: AuthorDAO = Depends(get_dao)) -> Response:
    services = AuthorService(dao)

    try:
        res = await services.search(param)

        return Response(status_code=status.HTTP_200_OK, content=json.dumps([u.serialize() for u in res]),
                        media_type="application/json")
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )




@AUTHOR_ROUTER.put("/", status_code=status.HTTP_201_CREATED)
async def update(entity: AuthorUpdate, dao: IAuthorDAO = Depends(get_dao)) -> Response:
    services = AuthorService(dao)

    try:
        res = await services.update(entity.cod, entity.description)  # faltaba cerrar paréntesis
        if res == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(entity))

        return Response(status_code=status.HTTP_201_CREATED)

    except Exception as ex:
        # Captura cualquier error inesperado
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )
@AUTHOR_ROUTER.post("/upload-image/{cod}")
async def upload_image(cod: str, file: UploadFile = File(...)) -> Response:
    # Validar que sea imagen
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Debe enviar una imagen válida")

    # Leer bytes originales
    original_bytes = await file.read()

    try:
        # Convertir a PNG usando PIL
        image = Image.open(io.BytesIO(original_bytes))
        png_bytes = io.BytesIO()
        image.convert("RGBA").save(png_bytes, format="PNG")
        png_bytes.seek(0)

        # Generar nombre final
        filename = f"{cod}.png"
        final_path = os.path.join(pathIMG, filename)

        # Guardar imagen
        with open(final_path, "wb") as f:
            f.write(png_bytes.getvalue())

        return Response(status_code=status.HTTP_201_CREATED,media_type="image/png")


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando imagen: {e}")

@AUTHOR_ROUTER.get("/{cod}/{width}/{height}")
async def get_author_image(cod: str, width: int=300, height: int=300):
    # Ruta de la imagen original
    image_path = os.path.join(pathIMG, f"{cod}.png")

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Imagen del autor no encontrada")

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