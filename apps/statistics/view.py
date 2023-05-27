from fastapi import APIRouter, Depends, Response
from services.connections import get_db
from apps.statistics import crud

router = APIRouter(
    prefix='/request',
    tags=['statistics ']
)


@router.get('/cities')
def cities(db=Depends(get_db)):
    return crud.cities(db)


@router.get('/categories')
def categories(db=Depends(get_db)):
    return crud.categories(db)


@router.get('/statistic_types')
def types():
    return Response(
        content=crud.statistic_types(),
        status_code=200
    )


@router.get('/statistics/{city_id}/{category_id}/{statistic_type}')
def statistics(city_id, category_id, statistic_type, db=Depends(get_db)):
    return Response(
        content=crud.get_city_category_statistic(city_id, category_id, statistic_type, db),
        status_code=200
    )
