""" Main module of mathTaker app
    Version 0.0.1 *

    todo: distinguish row index (starts at 0) and row number (starts at 1)
"""

import random
import json

from flask import Flask

from models import game_state

app = Flask(__name__)

rand = random.Random()
rand.seed(a=1)  # a=1 for reproducibility


class _Error(Exception):
    """Class for exceptions of this module. All these exceptions should be handled internally"""
    pass


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
        rows = game_state.GameState(list(rows_state)).get_rows()
        # choose a random move or quit
        if sum(rows) > 1:
            # random move
            non_zeros = [k for k in range(5) if rows[k] > 0]  # all indices with value > 0
            i = rand.choice(non_zeros)  # choose such index
            max_n = min(3, rows[i])  # max number of matches to be taken at this index
            if len(non_zeros) == 1:  # special case: only this row has matches --> must not take all
                max_n = min(max_n, rows[i] - 1)
            n = rand.randint(1, max_n)  # choose number of matches at this index
            result = {"row number": i + 1, "number of matches": n}
            assert sum(rows) - n > 0
            if sum(rows) - n == 1:
                result["end of game"] = "You lost! :-("
        else:
            # quit
            assert sum(rows) == 1
            result = {"end of game": "You won! :-)"}
    except (_Error, game_state.Error) as e:
        result["error"] = str(e)
    finally:
        pass  # no return here, see PEP 601
    # return result
    return json.dumps(result)


if __name__ == '__main__':
    app.run()
