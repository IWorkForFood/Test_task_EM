from sqlalchemy import insert, select
from app.students.models import TextReport
from app.database import async_session_maker
from app.dao.base import BaseDAO

class TextReportsDAO(BaseDAO):
    model = TextReport