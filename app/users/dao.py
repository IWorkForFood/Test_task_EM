from sqlalchemy import insert, select
from app.users.models import User
from app.database import async_session_maker
from app.dao.base import BaseDAO

class UserDAO(BaseDAO):
    model = User