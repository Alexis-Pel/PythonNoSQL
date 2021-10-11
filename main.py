import os

from flask import Flask

app = Flask(__name__)
host = os.environ["HOST"]


@app.route("/")
def print_hi():
    return '<h1>hi</h1>'


if __name__ == '__main__':
    app.run(
        host=host,
        port=8001,
        debug=True
    )
