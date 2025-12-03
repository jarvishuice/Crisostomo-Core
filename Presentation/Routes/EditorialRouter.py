import json

from fastapi import APIRouter, Response, status, HTTPException, Depends, UploadFile, File

from Domain.Entities.Editorial.EditorialEntity import EditorialEntity
from Infrastructure.DAO.Editorial.EditorialDAO import EditorialDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster

from Presentation.Services.EditorialService import EditorialService

EDITORIAL_ROUTER = APIRouter(
    prefix="/editorial",
    tags=["editorial"],

)


def get_dao():
    pool = PostgreSQLPoolMaster.get_instance()
    return EditorialDAO(pool)


@EDITORIAL_ROUTER.post("/")
async def create(entity: EditorialEntity, dao: EditorialDAO = Depends(get_dao)) -> Response:
    services = EditorialService(dao)
    try:
        res = await services.create_editorial(entity)
        if res is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No editorial found")
        return Response(status_code=status.HTTP_201_CREATED,
                        media_type="application/json")

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )


@EDITORIAL_ROUTER.get("/")
async def get(dao: EditorialDAO = Depends(get_dao)) -> Response:
    services = EditorialService(dao)
    try:
        res = await services.get_all_editorials()
        if len(res) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No editorial found")
        return Response(status_code=status.HTTP_200_OK, content=json.dumps([u.serialize() for u in res]),
                        media_type="application/json")

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )


@EDITORIAL_ROUTER.get("/{code}")
async def find_by_code(code: str, dao: EditorialDAO = Depends(get_dao)) -> Response:
    services = EditorialService(dao)
    try:
        res = await services.get_editorial(code)
        if res is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No editorial found")
        return Response(status_code=status.HTTP_200_OK, content=json.dumps(res.serialize()),
                        media_type="application/json")

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )
