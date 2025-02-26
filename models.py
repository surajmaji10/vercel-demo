
from main import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class TodoModel(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(100))
    description = Column(String(100))
    done = Column(Boolean)

