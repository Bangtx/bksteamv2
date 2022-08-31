# Use to run code on server
try:
    import unzip_requirements  # noqa: F401
except ImportError:
    pass

from fastapi import FastAPI, Request, status
# from fastapi.exceptions import RequestValidationError, HTTPException
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum
# from utils.auth import AuthError
# from utils.sns_handler import write_mess

from config.setting import APP_ENV, PROJECT_NAME, LANGUAGE, WEB_URL
from config.database import db

from core.api import api_router
import i18n
import os

# Load translation

i18n.load_path.append(os.path.dirname(os.path.realpath(__file__)) + "/langs")
i18n.set("locale", LANGUAGE)
i18n.set("file_format", "yml")

docs_url = "/docs" if APP_ENV == "dev" else None
redoc_url = "/redoc" if APP_ENV == "dev" else None
openapi_url = "/openapi.json" if APP_ENV == "dev" else None

app = FastAPI(
    title=f"{PROJECT_NAME} api",
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    if db.is_closed():
        db.connect()


@app.on_event("shutdown")
async def shutdown():
    if not db.is_closed():
        db.close()


app.include_router(api_router)

handler = Mangum(app)


