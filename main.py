import os

from flask import Flask

app = Flask(__name__)
host = os.environ["HOST"]


@app.route("/")
def print_hi():
    """
    Fonction affichant un titre 'Hi'
    :return: string : Hey You
    """
    return '<h1>Hey You !</h1>'


if __name__ == '__main__':
    app.run(
        host=host,
        port=8001,
        debug=True
    )
