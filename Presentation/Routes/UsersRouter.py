import json
from json import JSONEncoder
from typing import List

from fastapi import APIRouter, Response, status, HTTPException, Depends

from Domain.Entities.Users.UserEntity import UserEntity
from Infrastructure.DAO.Users.UserDAO import UserDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster

from Presentation.Services.UsersServices import UserServices

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
