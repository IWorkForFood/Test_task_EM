from sqlalchemy import insert, select
from .models import Reviews
from app.database import async_session_maker
from app.dao.base import BaseDAO

class ReviewsDAO(BaseDAO):
    model = Reviews