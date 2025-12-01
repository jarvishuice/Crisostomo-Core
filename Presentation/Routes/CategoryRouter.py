import json
from logging import getLogger
from fastapi import APIRouter, Response, status, HTTPException, Depends
from Infrastructure.DAO.Category.CategoryDAO import CategoryDAO
from Infrastructure.Providers.PostgreSQLPoolMaster import PostgreSQLPoolMaster


from Presentation.Services.CategoryService import CategoryService

CATEGORY_ROUTER = APIRouter(
    prefix="/category",
    tags=["category"],

)

def get_dao():
    pool = PostgreSQLPoolMaster.get_instance()
    return CategoryDAO(pool)


log = getLogger("AppLogger")


@CATEGORY_ROUTER.get("/areas", status_code=status.HTTP_200_OK)
async def getAreas(dao: CategoryDAO = Depends(get_dao)) -> Response:
    services = CategoryService(dao)
    try:
        res = await services.getAreas()
        print(res[0].name)
        return Response(status_code=status.HTTP_200_OK, content=json.dumps([u.serialize() for u in res]),
                        media_type="application/json")
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )

@CATEGORY_ROUTER.get("/filter/{parentCod}", status_code=status.HTTP_200_OK)
async def filterByParentCod(parentCod:str,dao: CategoryDAO = Depends(get_dao)) -> Response:
    services = CategoryService(dao)
    try:
        res = await services.getByParentCod(parentCod)
        print(res[0].name)
        return Response(status_code=status.HTTP_200_OK, content=json.dumps([u.serialize() for u in res]),
                        media_type="application/json")
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)

        )


