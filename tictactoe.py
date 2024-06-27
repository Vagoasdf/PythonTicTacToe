from flask import Flask
from flask import jsonify
from flask import request
from app.models import db, Game, Move
import json 

app = Flask(__name__)
# We're using sqlite so we dont need to worry about deploying a complete DB 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

with app.app_context():
    db.create_all()
    

@app.route("/")
def hello_world():
    return "<p>Tic Tac Toe Inicializado</p>"

@app.get("/api/game")
def game_get_all(): 
    return jsonify(getAllGames())

@app.post("/api/game")
def game_post():
    return jsonify(createGame())

@app.get("/api/game/<game_id>")
def game_get(game_id):
    return jsonify(getGame(game_id))

@app.post("/api/game/<game_id>/move")
def game_move_post(game_id):
    response=  makeMove(game_id, int(request.form['x']), int(request.form['y']))

    return jsonify(response)

def  getAllGames():
    games = Game.query.order_by(Game.created_at).all()
    gamesJson = [game.toJson() for game in games]

    return { 
        'message': 'Games Listed',
        'games': gamesJson,
    }

def createGame():
    game = Game();
    db.session.add(game)
    db.session.commit()
    return { 
        'message': 'Game Created',
        'game_id': game.id,
    }

def getGame(game_id):
    game = db.get_or_404(Game, game_id)
    return { 
        'message': 'Game Obtained',
        'game': game.detailedToJson()
    }

def makeMove(game_id, x, y):
    if  x > 2 or y > 2 or x < 0 or y < 0:
        return "Invalid position", 400
    game = db.get_or_404(Game, game_id)
    if game.status == 'finished':
        return "Game already finished", 400
    ## First Filter 
    invalidMove = db.session.query(Move.id).filter_by(gameId=game.id, coordX=x, coordY=y).first() is not None
    ## TODo, improve. We should get All the Moves from the Game and check from there, It will reduce DB Calls
    if invalidMove:
        return "Position already taken", 400
    
    newMovePlayer = Move(
        gameId = game.id,
        player = 'X',
        coordX = x,
        coordY = y,
    )
    db.session.add(newMovePlayer)

    ## check Victory
    if haveVictory(game, 'X'):
        game['status'] = 'finished'
        game['winner'] = 'Player (X)'
        db.session.add(game)
        db.session.commit()
        return 
    ## Computer moves
    newMoveComputer = makeMoveComputer(game)
    db.session.add(newMoveComputer)
    if haveVictory(game, 'O'):
        game['status'] = 'finished'
        game['winner'] = 'Computer (O)'

        db.session.add(game)
        db.session.commit()
        return 

    db.session.commit()

    response = {
        'message': 'Moving '+request.form['x']+request.form['y'],
        'game': game.detailedToJson()
    }
    return response

def getGameFromDB(game_id):
    return {
        'id': game_id,
        'board': [
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ],
        'current_player': 'X',
        'status': 'ongoing'
    }

def haveVictory(game, player):
    return False

def makeMoveComputer(game):
    ## For Now, 1 to 1. 
    ## Pending Implementation to check for collission
    return  Move(
        gameId = game.id,
        player = 'O',
        coordX = 1,
        coordY = 1,
    )