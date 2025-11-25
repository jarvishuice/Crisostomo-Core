import json
from json import JSONEncoder
from typing import List

from fastapi import APIRouter, Response, status, HTTPException, Depends

from Domain.Entities.Users.UserEntity import UserEntity
from Infrastructure.DAO.Users.UserDAO import UserDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster
from Presentation.DTOS.Auth.LoginRequest import LoginRequest
from Presentation.DTOS.Reponse.ResponseAPI import ApiResponse
from Presentation.MIddleWare.BearerAuth import require_token
from Presentation.Services.AuthService import AuthService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


AUTH_ROUTER = APIRouter(
    prefix="/AUTH",
    tags=["AUTORIZATION" ]
)
def get_dao():
    pool = PostgreSQLPoolMaster.get_instance()
    return UserDAO(pool)



@AUTH_ROUTER.post("/login", status_code=status.HTTP_200_OK)
async def login(entity: LoginRequest,dao: UserDAO = Depends(get_dao))-> Response:
    services = AuthService(dao)

    try:
        res = await services.login(entity.username,entity.password)  # faltaba cerrar paréntesis


        return Response(status_code=status.HTTP_200_OK,content=res)

    except Exception as ex:
        # Captura cualquier error inesperado
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )


@AUTH_ROUTER.get("/me", status_code=status.HTTP_200_OK)
async def get_user(jwt_data=Depends(require_token), dao: UserDAO = Depends(get_dao)):
    services = AuthService(dao)
    print(jwt_data)

     # 'sub' es el cod del usuario
    res = await services.getCurrentUser(jwt_data)
    print(res)


    return Response(
         media_type="application/json",
         status_code=status.HTTP_200_OK,
         content=json.dumps(
             ApiResponse(success=True, message="Validación realizada con éxito", data=res).dict()
         )
     )
