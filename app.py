import random
import json
from flask import Flask

app = Flask(__name__)

rand = random.Random()
rand.seed(a=1) # a=1 for reproducibility

@app.route('/')
def hello_world():
    return 'Hello from MatchTaker. Currently only API!'

"""
/nextmove [/<gamestate> [/<level>] ]
Examples:
    /nextmove
    /nextmove/10340
    /nextmove/10340/2
<gamestate> is a sequence of digits of 0..5. Digit at position k must be <= k (where first position means k=1)
<level> is integer in 0..2
"""
@app.route('/nextmove',defaults={'gamestate': '12345', 'level': 1})
@app.route('/nextmove/<string:gamestate>',defaults={'level': 1})
@app.route('/nextmove/<string:gamestate>/<int:level>')
def nextmove(gamestate, level):
    intlist = [int(x) for x in list(gamestate)]
    y = level

    # assuming input consistent

    # quit or choose a random move
    dict = None
    if sum(intlist) == 1:
        # quit
        dict = {"end of game" : "You won! :-)"}
    else:
        # random move
        nonzeros = [k for k in range(5) if intlist[k] > 0] # all indices with value > 0
        i = rand.choice(nonzeros)  # choose such index
        maxn = min(3,intlist[i]) # max number of matches to be taken at this index
        if len(nonzeros) == 1: # special case: only this row has matches --> must not take all
            maxn = min(maxn,intlist[i]-1)
        n = rand.randint(1,maxn) # choose number of matches at this index
        dict = {"row number":i+1, "number of matches":n}
        assert sum(intlist) - n > 0
        if sum(intlist) - n == 1:
            dict["end of game"] = "I won! :-("
    #return result
    return json.dumps(dict)

if __name__ == '__main__':
    app.run()
