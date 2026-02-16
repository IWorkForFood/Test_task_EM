from fastapi import FastAPI, File, UploadFile
from app.users.router import router_user
from .database import async_session_maker 
from sqlalchemy import text, insert
import uuid
import datetime
import os


app = FastAPI()

app.include_router(router_user)
