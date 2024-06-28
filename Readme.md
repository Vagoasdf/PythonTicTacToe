# TicTacToe

## Description
TicTacToe is a classic game played on a 3x3 grid. The objective of the game is to get three of your own symbols (either X or O) in a row, either horizontally, vertically, or diagonally.

This project is an implementation of the TicTacToe game in Python. It provides an API interface for players to play against the computer. Currently, the computer only picks the moves randomly, Future improvments can be made for the computer AI. 

## Features
- Error handling for invalid moves
- Win detection and game over condition
- Historic game database

## Installation
1. Clone the repository: `git clone [repository URL]`
2. Navigate to the project directory: `cd TicTacToe`
3. Install the necessary libraries with pip install -r requirements.txt
4. Start the App with flask --app tictactoe run
5. Enjoy!

## Usage
1. Start by creating a new TicTacToe Game with a POST call on /api/game
2. Make your moves with a POST call on /api/game/[gameId]/move
3. If you want to check the games history, make a GET call on /api/game
4. If you want to check an specific game, make a GET call on /api/game/[gameId] 

## Timetable spent
* 1 Hour - Researching. Planning the solution and architecture. Building the base app
* 2 Hours -  Building the base App Endpoints, Creating games, basic of creating moves, connecting to the sqlite database 
* 1 Hour - Wild chase trying to use Recursive functions and Linked List on the Moves. Not reflected on the final code
* 1 Hour - Base solution using List and simple for loops. Cleaning up the code, commenting. 

## Assumptions
* Human player always moves First
* The board is always a 3x3 board. 
* When we check for the game, we do not want to see the board for all the moves, but only the final board, and the historic of moves

## Trade Offs
* The makeMove can be improved. DB calls for all the moves could be done in a more elegant way. Could spend a few more hours cleaning up 
* The makeMoveComputer can be expensive on DB calls, since we are doing random moves, and checking each of these moves with the database. This might be solved with a clever loop throught the board, instead of calling the DB. However, for time constrains, the DB Solution was prefered