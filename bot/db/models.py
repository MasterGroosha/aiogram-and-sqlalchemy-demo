from sqlalchemy import Column, Integer, BigInteger

from bot.db.base import Base


class PlayerScore(Base):
    __tablename__ = "playerscore"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    score = Column(Integer, default=0)
