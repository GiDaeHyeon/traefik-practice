from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from model.conn import engine, Base
from model.table import *
from router.v0 import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/v0")
