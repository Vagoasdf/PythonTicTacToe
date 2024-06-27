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

    def toJson(self):  
       return {
            'id': self.id,
            'status': self.status,
            'date': self.created_at
        } 
    
    ## Todo: should also return the Moves of the Game object
    def detailedToJson(self):
       return "" 
class Move(db.Model):
    __tablename__ = 'moves'
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=db.func.current_timestamp())
    gameId: Mapped[int] = mapped_column(ForeignKey('games.id'))
    prevMoveId: Mapped[Optional[int]] = mapped_column(ForeignKey('moves.id'))
    nextMoveId: Mapped[Optional[int]] = mapped_column(ForeignKey('moves.id'))
    coordX: Mapped[int]
    coordY: Mapped[int]

    def toJson(self):  
       return {
            'id': self.id,
            'gameId': self.gameId,
            'x': self.coordX,
            'y': self.coordY
        }

