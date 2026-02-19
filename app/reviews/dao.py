from sqlalchemy import insert, select
from .models import Review
from app.database import async_session_maker
from app.dao.base import BaseDAO

class ReviewDAO(BaseDAO):
    model = Review