"""Main module of matchTaker app.

Version 0.0.1 *
The following URLs are served:

"/" : just a message hinting to API
"/next_move" : to compute a next move in the game
"""
# todo: distinguish row index (starts at 0) and row number (starts at 1)


import json

from flask import Flask

from models import solver, game_states
from models.game_states import GameState, GameMove
from models.game_trees import set_current_tree

app = Flask(__name__)


@app.route('/')
def hello_world():
    """Main page, currently empty."""
    return 'Hello from MatchTaker. Currently only API!'


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
    <rows_state> is a sequence of digits of 0..5. Digit at index k must be <= k+1 (where first index is k=0)
    <level> is integer in 0..2

    Response:
    Will be changed, see todo

    """
    # todo: return only game-move and game-continue in response, no text
    result = {}
    try:
        # check and convert input
        rows = list(rows_state)
        game_states.Error.check(all([('0' <= rows[k] <= '5') for k in range(len(rows))]),
                                "rows_state must contain digits in 0..5")
        rows = [int(rows[k]) for k in range(len(rows))]
        game_state = GameState(rows)
        # compute next move
        game_move, game_continues = solver.solve(game_state, level)
        # compose result
        if game_continues == -1:
            result = {"end of game": "You won! :-)"}
        else:
            result = {"row index": game_move.row_index, "number of matches": game_move.match_count}
            if game_continues == 0:
                result["end of game"] = "You lost! :-("
            else:
                result["game continues"] = game_continues
    except (solver.Error, game_states.Error) as e:
        result["error"] = str(e)
    finally:
        pass  # no return here, see PEP 601
    # return result
    return json.dumps(result)


if __name__ == '__main__':
    set_current_tree(GameState([1, 2, 3, 4, 5]))
    app.run()
