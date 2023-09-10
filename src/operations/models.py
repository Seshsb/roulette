from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from users.models import User


class Cell(Base):
    __tablename__ = 'cells'
    id = Column(Integer, primary_key=True)
    weight = Column(Integer)
    logs = relationship('Log')


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    cell_id = Column(Integer, ForeignKey('cells.id'))
    round_id = Column(Integer)
    user = relationship('User')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
