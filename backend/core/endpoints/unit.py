from fastapi import APIRouter
import models.unit as models
import schemas.unit as schemas


router = APIRouter()


@router.get('/')
def get_units(classroom: int):
    return models.Unit.get_units(classroom)


@router.post('/')
def create_schedule(schedule: schemas.ScheduleCreate):
    return models.Unit.create(**schedule.dict())


@router.put('/{id}')
def update_schedule(id: int, schedule: schemas.ScheduleUpdate):
    return models.Unit.update_one(id, schedule.dict())


@router.delete('/{id}')
def delete_schedule(id: int):
    return models.Unit.soft_delete(id)
