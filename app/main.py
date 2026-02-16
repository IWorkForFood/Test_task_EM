from fastapi import FastAPI, File, UploadFile
from app.students.router import router_textreports as router_txtr
from app.users.router import router_user
from app.user_customization.router import router_user_customization
from fastapi.responses import FileResponse
from .students.models import TextReport
from .students.shemas import STextReport
from .users.models import User
#from .users.shemas import SUser
from .user_customization.models import TypicalData
from .user_customization.shemas import STypicalData
from .database import async_session_maker 
from sqlalchemy import text, insert
import uuid
import datetime
import os


app = FastAPI()

app.include_router(router_txtr)
app.include_router(router_user)
app.include_router(router_user_customization)
