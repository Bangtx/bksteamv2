from fastapi import APIRouter, Depends
from core.endpoints import (
    auth,
    import_data,
    student,
    teacher,
    classroom,
    unit,
    slide,
    roll_call,
    score,
    notification,
    home_work,
    self_learning,
    home_work_result,
    home_work_file,
    home_work_file_result,
    csv
)


api_router = APIRouter()
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwibmFtZSI6ImJhbmcifQ.S2dAxQIiKowun1gwPdOoNy3vnTXDrJvEr-dWVwjSbpc
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(import_data.router, prefix='/import_data', tags=['import_data'])
api_router.include_router(teacher.router, prefix='/teacher', tags=['teacher'])
api_router.include_router(student.router, prefix='/student', tags=['student'])
api_router.include_router(classroom.router, prefix='/classroom', tags=['classroom'])
# api_router.include_router(class_time.router, prefix='/class_time', tags=['class_time'])
api_router.include_router(roll_call.router, prefix='/roll_call', tags=['roll_call'])
# api_router.include_router(absent_type.router, prefix='/absent_type', tags=['absent_type'])
api_router.include_router(score.router, prefix='/score', tags=['score'])
api_router.include_router(notification.router, prefix='/notification', tags=['notification'])
api_router.include_router(home_work.router, prefix='/home_work', tags=['home_work'])
api_router.include_router(home_work_file.router, prefix='/home_work_file', tags=['home_work_file'])
api_router.include_router(home_work_result.router, prefix='/home_work_result', tags=['home_work_result'])
api_router.include_router(home_work_file_result.router, prefix='/home_work_file_result', tags=['home_work_file_result'])
# api_router.include_router(question_student.router, prefix='/home_work_student', tags=['home_work_student'])
# api_router.include_router(question.router, prefix='/question', tags=['question'])
api_router.include_router(unit.router, prefix='/unit', tags=['unit'])
# api_router.include_router(audio_file.router, prefix='/audio_file', tags=['audio_file'])
# api_router.include_router(file_question.router, prefix='/file_question', tags=['file_question'])
# api_router.include_router(home_work_file.router, prefix='/home_work_file', tags=['home_work_file'])
api_router.include_router(slide.router, prefix='/slide', tags=['slide'])
# api_router.include_router(file_result_student.router, prefix='/file_result_student', tags=['file_result_student'])
api_router.include_router(self_learning.router, prefix='/self_learning', tags=['self_learning'])
api_router.include_router(csv.router, prefix='/csv', tags=['csv'])
