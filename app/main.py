from fastapi import FastAPI, File, UploadFile
from app.users.router import router_user
from .database import async_session_maker 
from sqlalchemy import text, insert
import uuid
import datetime
import os
from app.users.models import User
from app.reviews.models import Review
from app.products.models import Product
from app.order.models import Order

app = FastAPI()

app.include_router(router_user)
