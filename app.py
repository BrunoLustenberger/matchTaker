from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello from MatchTaker. Currently only API!'


@app.route('/nextmove',defaults={'gamestate': '12345', 'level': 1})
@app.route('/nextmove/<string:gamestate>',defaults={'level': 1})
@app.route('/nextmove/<string:gamestate>/<int:level>')
def nextmove(gamestate, level):
    intlist = [int(x) for x in list(gamestate)]
    y = level
    return "blabla"

if __name__ == '__main__':
    app.run()
