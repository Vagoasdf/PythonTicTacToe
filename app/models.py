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
    winner: Mapped[Optional[str]] = mapped_column(default=None)

    def toJson(self):  
       return {
            'id': self.id,
            'status': self.status,
            'date': self.created_at,
            'winner': self.winner,
        } 
    
    ## Todo: should also return the Moves of the Game object
    def detailedToJson(self):
       moves = Move.query.filter(Move.gameId == self.id).order_by(Move.created_at).all()
       movesJson = [move.toJson() for move in moves]

       return  {
            'id': self.id,
            'status': self.status,
            'date': self.created_at,
            'winner': self.winner,
            'moves': movesJson,
        } 
class Move(db.Model):
    __tablename__ = 'moves'
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=db.func.current_timestamp())
    gameId: Mapped[int] = mapped_column(ForeignKey('games.id'))
    prevMoveId: Mapped[Optional[int]] = mapped_column(ForeignKey('moves.id'))
    nextMoveId: Mapped[Optional[int]] = mapped_column(ForeignKey('moves.id'))
    player: Mapped[str] = mapped_column(default='X')
    coordX: Mapped[int]
    coordY: Mapped[int]

    def toJson(self):  
       return {
            'id': self.id,
            'gameId': self.gameId,
            'player': self.player,
            'x': self.coordX,
            'y': self.coordY
        }

