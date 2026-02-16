from fastapi import APIRouter, Depends, Response, HTTPException, status, BackgroundTasks
from sqlalchemy import select 
from app.database import async_session_maker 
from app.users.models import User
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from .auth_utils import get_auth_data, get_password_hash, authenticate_user, create_access_token
from .dependencies import get_current_user
from .models import User
from .shemas import SRegisterUser, SAuthUser
from sqlalchemy import text, insert
from .dao import UserDAO
from pydantic import EmailStr
from app.exceptions import TokenExpiredException
import uuid
import datetime
import os

router_user = APIRouter(prefix='/permissions', tags=['Работа с правами доступа'])


    
