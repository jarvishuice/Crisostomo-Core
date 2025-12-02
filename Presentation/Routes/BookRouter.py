import io
import json
import os
from logging import getLogger
from fastapi import APIRouter, Response, status, HTTPException, Depends, UploadFile, File

from Domain.Entities.Book.BookEntity import BookEntity
from Infrastructure.DAO.Book.BookDAO import BookDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster

from Presentation.Services.BookService import BookService

BOOK_ROUTER = APIRouter(
    prefix="/book",
    tags=["book"],

)


def get_dao():
    pool = PostgreSQLPoolMaster.get_instance()
    return BookDAO(pool)


log = getLogger("AppLogger")


@BOOK_ROUTER.post("/", status_code=status.HTTP_200_OK)
async def create(book: BookEntity, dao: BookDAO = Depends(get_dao)) -> Response:
    services = BookService(dao)
    try:
        res = await services.save(book)

        return Response(status_code=status.HTTP_201_CREATED,
                        media_type="application/json")
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )
@BOOK_ROUTER.get("/", status_code=status.HTTP_200_OK)
async def get(size:int=100,page:int=1, dao: BookDAO = Depends(get_dao)) -> Response:
    services = BookService(dao)
    try:
        res = await services.get_books(size,page)

        return Response(status_code=status.HTTP_200_OK,
                        media_type="application/json",
                        content=json.dumps([u.serialize() for u in res]))
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )
@BOOK_ROUTER.get("/filter/category/{category}", status_code=status.HTTP_200_OK)
async def filterByCategory(category:str, dao: BookDAO = Depends(get_dao)) -> Response:
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
async def filterByArea(area:str, dao: BookDAO = Depends(get_dao)) -> Response:
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
async def filterBySubArea(subArea:str, dao: BookDAO = Depends(get_dao)) -> Response:
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
