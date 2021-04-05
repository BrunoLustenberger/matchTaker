"""Main module of matchTaker app.

Version 0.0.1 *
The following URLs are served:

"/" : just a message hinting to API
"/next_move" : to compute a next move in the game
"""
# todo: distinguish row index (starts at 0) and row number (starts at 1)


import json

from flask import Flask, render_template
# from flask_talisman import Talisman

import logging
from utils import mylogconfig

from models import solver, game_states
from models.game_states import GameState  # , GameMove
from models.game_trees import set_current_tree

app = Flask(__name__)
# Talisman(app)


@app.route('/')
def home_page():
    """Home page."""
    logging.info("home_page")
    return render_template('home.html')


@app.route('/rules')
def rules_page():
    """rules page."""
    logging.info("rules_page")
    return render_template('rules.html')


@app.route('/settings')
def settings_page():
    """settings page."""
    logging.info("settings_page")
    return render_template('settings.html')


@app.route('/about')
def about_page():
    """about page."""
    logging.info("about_page")
    return render_template('about.html')


@app.route('/email')
def email_page():
    """email page."""
    logging.info("email_page")
    return render_template('email.html')


@app.route('/next_move', defaults={'rows_state': '12345', 'level': 0})
@app.route('/next_move/<rows_state>', defaults={'level': 0})
@app.route('/next_move/<rows_state>/<int:level>')
def next_move(rows_state, level):
    """Compute the next move from a given state.

    Method: GET

    Request:
    /next_move [/<rows_state> [/<level>] ]
    Examples:
        /next_move
        /next_move/10340
        /next_move/10340/2
    <rows_state> is a sequence of digits of 0..5.
    Digit at index k must be <= k+1 (where first index is k=0).
    <level> is integer in 0..2

    Response: see also doc of return value of solver.solve.
        One of the 3 json strings:
        1. {“gameContinues“:-1}
           Meaning: "You won".
        2. {“gameContinues“:c, "rowIndex":i, "numberOfMatches":n}
           where c in 0..3, i in 0..4, n in 1..3.
           Meaning:
             The move of the app is taking n matches from the row with index i.
             c == 0: "the App won". There is only 1 match left.
             c == 1: game continues, i.e. more than 1 match left. No further information.
             c == 2: game continues and you have a safe strategy to win.
             c == 3: game continues and your opponent (the App) has a safe strategy to win.
        3. {"error" : message}
           where message is a string describing the error.
           Meaning:
           A software error occurred while the app executed the request.
    """
    result = {}
    try:
        # log
        logging.info(f"next_move, rows {rows_state}, level {level}")
        # check and convert input
        rows = list(rows_state)
        game_states.Error.check(all([('0' <= rows[k] <= '5') for k in range(len(rows))]),
                                "rows_state must contain digits in 0..5")
        rows = [int(rows[k]) for k in range(len(rows))]
        game_state = GameState(rows)
        # compute next move
        game_move, game_continues = solver.solve(game_state, level)
        # compose result
        result["gameContinues"] = game_continues
        if game_continues >= 0:
            result["rowIndex"] = game_move.row_index
            result["numberOfMatches"] = game_move.match_count
    except (solver.Error, game_states.Error) as e:
        result["error"] = str(e)
    finally:
        pass  # no return here, see PEP 601
    # return result
    logging.info(f"next_move, result {result}")
    return json.dumps(result)


mylogconfig.simplest()
set_current_tree(GameState([1, 2, 3, 4, 5]))

if __name__ == '__main__':
    app.run()
