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
    response =  makeMove(game_id, int(request.form['x']), int(request.form['y']))
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

    if Move.checkInvalidMove(x,y,game,):
        return "Position already taken", 400
    
    AllMoves = db.session.query(Move).filter_by(gameId=game.id).order_by(Move.id).all()

    newMovePlayer = Move(
        gameId = game.id,
        player = 'X',
        coordX = x,
        coordY = y,
    )

    db.session.add(newMovePlayer)
    AllMoves.append(newMovePlayer)
    board = buildBoard(AllMoves)

    ## check Victory
    if haveVictory(board, 'X'):
        game.status = 'finished'
        game.winner = 'Player (X)'
        db.session.add(game)
        db.session.commit()
        return buildResponse(game,board)

    
    ## All 9 Squares are  filled. It's a Draw
    if len(AllMoves) == 9:
        game.status = 'finished'
        game.winner= 'Draw'
        db.session.add(game)
        db.session.commit()
        return buildResponse(game,board)
 
    
    ## Computer moves
    newMoveComputer = makeMoveComputer(game)
    db.session.add(newMoveComputer)
    addToBoard(board, newMoveComputer)
    if haveVictory(board, 'O'):
        game.status = 'finished'
        game.winner = 'Computer (O)'
        db.session.add(game)
        db.session.commit()
        return buildResponse(game,board)
 

    db.session.commit()
    return buildResponse(game,board)

def buildResponse(game,board):
    return { 
        'game': game.detailedToJson(),
        'board': board
    }
def getBlankBoard():
    return  [
        ['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ]
    

def buildBoard(moves):
    baseBoard = getBlankBoard()
    for move in moves:
        baseBoard[move.coordX][move.coordY] = move.player
    return baseBoard
    

def addToBoard(board,move):
    board[move.coordX][move.coordY] = move.player

def haveVictory(board, player):
    boardRange = range(3) #list for iterating.
    ## Check rows (and columns)
    for row in boardRange:
        if (board[row][0] == board[row][1] == board[row][2] == player) or \
           (board[0][row] == board[1][row] == board[2][row] == player):
            return True
    ## Check the two diagonals.
    if (board[0][0] == board[1][1] == board[2][2] == player) or \
        (board[0][2] == board[1][1] == board[2][0] == player):
        return True 
    
    return False  # no victory yet.


def makeMoveComputer(game):
    ## For Now, 1 to 1. 
    ## Pending Implementation to check for collission
    ##if Move.checkInvalidMove(x,y,game,):
    return  Move(
        gameId = game.id,
        player = 'O',
        coordX = 1,
        coordY = 1,
    )