import models.image as models
import schemas.image as schemas
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get('/')
def get_image(path: str):
    return FileResponse(path)