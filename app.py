from boggle import Boggle
from flask import Flask, request, render_template, redirect, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Sunniva046'

boggle_game = Boggle()


@app.route('/')
def game_board():
    """display the game board"""
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('display-board.html', board=board)


@app.route('/check-word')
def check_word():
    """Check if word is in dict"""
    word = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board, word)

    return jsonify({'result': res})


@app.route('/post-score', methods=['POST'])
def post_score():
    """Post scores and update plays"""
    score = request.json['score']
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    session['highscore'] = max(score, highscore)
    session['nplays'] = nplays + 1

    return jsonify(brokenRecord=score > highscore)
