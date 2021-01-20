""" Main module of mathTaker app
    Version 0.0.1 *

    todo: distinguish row index (starts at 0) and row number (starts at 1)
"""

import json

from flask import Flask

from models import game_states, solver

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello from MatchTaker. Currently only API!'


@app.route('/next_move', defaults={'rows_state': '12345', 'level': 1})
@app.route('/next_move/<rows_state>', defaults={'level': 1})
@app.route('/next_move/<rows_state>/<int:level>')
def next_move(rows_state, level):
    """
    /next_move [/<rows_state> [/<level>] ]
    Examples:
        /next_move
        /next_move/10340
        /next_move/10340/2
    <rows_state> is a sequence of digits of 0..5. Digit at index k must be <= k+1 (where first index is k=0)
    <level> is integer in 0..2
    """
    result = {}
    try:
        # check and convert input
        game_state = game_states.GameState(list(rows_state))
        # compute next move
        row_index, match_count, game_continues = solver.solve(game_state, level)
        # compose result
        if not game_continues and match_count == 0:
            result = {"end of game": "You won! :-)"}
        else:
            result = {"row index": row_index, "number of matches": match_count}
            if not game_continues:
                result["end of game"] = "You lost! :-("
    except (solver.Error, game_states.Error) as e:
        result["error"] = str(e)
    finally:
        pass  # no return here, see PEP 601
    # return result
    return json.dumps(result)


if __name__ == '__main__':
    app.run()
