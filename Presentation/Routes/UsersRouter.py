import json
from json import JSONEncoder
from typing import List
import io
from fastapi import APIRouter, Response, status, HTTPException, Depends

from Domain.Entities.Users.UserEntity import UserEntity
from Infrastructure.DAO.Users.UserDAO import UserDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster
from Config.Settings import Settings
from fastapi.responses import StreamingResponse
from PIL import Image
from Presentation.Services.UsersServices import UserServices
import os
se = Settings()
pathIMG = se.USER_PROFILE_IMG_PATH
os.makedirs(pathIMG, exist_ok=True)
USER_ROUTER = APIRouter(
    prefix="/users",
    tags=["users", "usuarios"]
)
def get_dao():
    pool = PostgreSQLPoolMaster.get_instance()
    return UserDAO(pool)



@USER_ROUTER.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(entity: UserEntity,dao: UserDAO = Depends(get_dao)):
    services = UserServices(dao)

    try:
        res = await services.createUser(entity)  # faltaba cerrar paréntesis
        if res:
            # Devuelve 201 sin cuerpo, o puedes devolver el objeto creado
            return Response(status_code=status.HTTP_201_CREATED)
        else:
            # Si no se creó, lanza excepción controlada
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo crear el usuario"
            )
    except Exception as ex:
        # Captura cualquier error inesperado
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )

@USER_ROUTER.get("/", status_code=status.HTTP_200_OK)
async def GETAkk(dao: UserDAO = Depends(get_dao)):
    services = UserServices(dao)

    try:
        res = await services.GetAllUsers()  # faltaba cerrar paréntesis

        if res:
            # Devuelve 201 sin cuerpo, o puedes devolver el objeto creado

            return Response(status_code=status.HTTP_200_OK,content=json.dumps([u.serialize() for u in res]),
                            media_type="application/json",)
        else:
            # Si no se creó, lanza excepción controlada
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se ENCONTRARON usuarios"
            )
    except Exception as ex:
        # Captura cualquier error inesperado
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )
@USER_ROUTER.get("/profile/picture/{code}/{width}/{height}", status_code=status.HTTP_200_OK)
async def getProfilePicture(code:str,width:int=100,height:int=100,dao: UserDAO = Depends(get_dao)):
    image_path = os.path.join(pathIMG, f"{code}.png")
    if not os.path.exists(image_path):
       image_path = os.path.join(pathIMG,f"default.png")

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