from sqlalchemy import insert, select
from app.user_customization.models import TypicalData
from app.database import async_session_maker
from app.dao.base import BaseDAO

class TypicalDataDAO(BaseDAO):
    model = TypicalData