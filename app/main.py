from fastapi import FastAPI, File, UploadFile
from app.users.router import router_user
from .products.router import products_router
from .permissions.router import router as permissions_router
from .reviews.router import router_reviews
from .order.router import router_orders
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
app.include_router(products_router)
app.include_router(permissions_router)
app.include_router(router_reviews)
app.include_router(router_orders)
