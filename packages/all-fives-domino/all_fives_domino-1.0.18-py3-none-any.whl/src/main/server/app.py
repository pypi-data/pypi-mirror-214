from flask import Flask, send_from_directory
import json

from src.main.game.Game import Game, GameStatus
from src.main.game.Brain import AllFivesGreedyBrain, PlayerBrain

app = Flask(__name__)

player_brain = PlayerBrain()
game = Game(AllFivesGreedyBrain(), AllFivesGreedyBrain())


@app.route("/")
def get_page():
    return send_from_directory("static", "index.html")


@app.route("/status")
def get_status():
    return game.json()


@app.route("/start")
async def start_game():
    global game

    game = Game(AllFivesGreedyBrain(), AllFivesGreedyBrain())
    game.run()
    return "OK"


@app.route("/play/<option>")
def player_decision(option: str):
    player_brain.decision = int(option)
    return "OK"
