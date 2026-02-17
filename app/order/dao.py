from sqlalchemy import insert, select
from .models import Product
from app.database import async_session_maker
from app.dao.base import BaseDAO

class OrderDAO(BaseDAO):
    model = Product