from typing import List
from fastapi import APIRouter
import schemas.roll_call as schemas
import models.roll_call as models
from utils.db import transaction
from playhouse.shortcuts import model_to_dict


router = APIRouter()


@router.get('/')
def get_roll_call(classroom: int, student=None):
    dates = list(
        models.RollCall.select(
            models.RollCall.date
        ).where(
            models.RollCall.active, models.RollCall.classroom == classroom
        ).order_by(
            models.RollCall.date.asc()
        ).dicts()
    )
    dates = list(set(list(map(lambda x: x['date'], dates))))
    data = []
    for date in dates:
        data.append({
            'date': date,
            'roll_call': models.RollCall.get_roll_call_by_date(date, classroom, student)
        })
    return data


@router.post('/')
@transaction
def update_roll_call(roll_call: schemas.RollCallCreate):
    roll_call = roll_call.dict()
    result = []
    for student_id, roll_call_id in roll_call['payload'].items():
        rc = models.RollCall.get_or_none(
            date=roll_call['date'],
            teacher=roll_call['teacher'],
            classroom=roll_call['classroom'],
            student=student_id
        )
        if rc:
            rc = models.RollCall.update_one(rc.id, {
                'date': roll_call['date'],
                'teacher': roll_call['teacher'],
                'classroom': roll_call['classroom'],
                'student': student_id,
                'absent_type': roll_call_id
            })
        else:
            rc = models.RollCall.create(
                date=roll_call['date'],
                teacher=roll_call['teacher'],
                classroom=roll_call['classroom'],
                student=student_id,
                absent_type=roll_call_id
            )
        result.append(model_to_dict(rc))
    return result


# @router.post('/create_roll_calls')
# def create_roll_call(roll_call: List[schemas.RollCallCreate]):
#     roll_call_data = list(map(lambda x: x.dict(), roll_call))
#     return list(
#         models.RollCall.insert_many(roll_call_data).dicts().execute()
#     )
#
#
# @router.put('/')
# def update(roll_call: schemas.RollCallUpdate):
#     roll_call_inserted = models.RollCall.get_or_none(
#         classroom=roll_call.classroom,
#         date=roll_call.date,
#         student=roll_call.student,
#         teacher=roll_call.teacher,
#     )
#
#     if roll_call_inserted:
#         return models.RollCall.update_one(roll_call_inserted.id, roll_call.dict())
#
#     return models.RollCall.create(**roll_call.dict())
