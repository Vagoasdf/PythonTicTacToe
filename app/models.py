from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import Optional

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Game(db.Model):
    __tablename__ = 'games'
    id: Mapped[int] = mapped_column(primary_key=True) 
    created_at: Mapped[datetime] = mapped_column(default=db.func.current_timestamp())
    status: Mapped[str] = mapped_column(default='pending')

class Move(db.Model):
    __tablename__ = 'moves'
    id: Mapped[int] = mapped_column(primary_key=True)
    gameId: Mapped[int] = mapped_column(ForeignKey('games.id'))
    prevMoveId: Mapped[Optional[int]] = mapped_column(ForeignKey('moves.id'))
    nextMoveId: Mapped[Optional[int]] = mapped_column(ForeignKey('moves.id'))
    coordX: Mapped[int]
    coordY: Mapped[int]
