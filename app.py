import random
import json
from flask import Flask

app = Flask(__name__)

rand = random.Random()
rand.seed(a=1)  # a=1 for reproducibility


class Error(Exception):
    """Class for exceptions of this module. All these exceptions should be handled internally"""
    pass


@app.route('/')
def hello_world():
    return 'Hello from MatchTaker. Currently only API!'


@app.route('/next_move', defaults={'game_state': '12345', 'level': 1})
@app.route('/next_move/<game_state>', defaults={'level': 1})
@app.route('/next_move/<game_state>/<int:level>')
def next_move(game_state, level):
    """
    /next_move [/<game_state> [/<level>] ]
    Examples:
        /next_move
        /next_move/10340
        /next_move/10340/2
    <game_state> is a sequence of digits of 0..5. Digit at position k must be <= k (where first position means k=1)
    <level> is integer in 0..2
    """
    result = None  # dictionary
    try:
        # check and convert input
        if len(game_state) != 5:
            raise Error('game_state must be 5 characters long')
        rows = []
        for k in range(5):
            c = game_state[k]
            if not ('0' <= c <= '5'):
                raise Error('game_state must consist of digits in 0..5')
            x = int(c)
            if not (x <= k+1):
                raise Error(f"row {k+1} must contain <= {k+1} matches")
            rows.append(x)
        if sum(rows) == 0:
            raise Error('game_state must contain at least 1 match')
        if not (level in range(3)):
            raise Error('level must be in 0..2')
        # quit or choose a random move
        if sum(rows) == 1:
            # quit
            result = {"end of game": "You won! :-)"}
        else:
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
                result["end of game"] = "I won! :-("
    except Error as e:
        result["error"] = str(e)
    finally:
        # return result
        return json.dumps(result)


if __name__ == '__main__':
    app.run()
