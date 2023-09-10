from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    round_id = Column(Integer, default=1)
    logs = relationship('Log')
