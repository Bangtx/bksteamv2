import models.image as models
import schemas.image as schemas
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get('/')
def get_audio(path: str):
    return FileResponse(path)