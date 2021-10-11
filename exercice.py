import os

import flask
from flask import Flask
from flask import request

app = Flask(__name__)
host = os.environ["HOST"]


@app.route("/")
def main():
    """
    Fonction affichant un titre 'Hi'
    :return: string : Hey You
    """
    return flask.make_response('<h1>Hey You !</h1>', 200)


@app.route("/users", methods=["GET", "POST", "PATCH", "DELETE"])
def users():
    try:
        name_arg = request.args['name']
    except:
        name_arg = None
    try:
        last_name_arg = request.args['last_name']
    except:
        last_name_arg = None
    try:
        id_arg = int(request.args['id'])
    except:
        id_arg = None

    if request.method == "GET":
        user_list = []
        for file in os.listdir("users"):
            with open(os.path.join("users", file), 'r') as f:
                user = f.readlines()
                last_name, name = user[0][0:-1], user[1]
                title = file.title().split('.')[0]
                user_list.append({"id": title, "last_name": last_name, "name": name})
        return str(list(reversed(user_list)))

    elif request.method == "POST":
        if name_arg is None:
            return "Prénom Incorrect"
        if last_name_arg is None:
            return "Nom Incorrect"
        if id_arg is None:
            return "Id Incorrect"
        try:
            open(os.path.join("users", f'{id_arg}.txt'))
            return "Utilisateur déja existant"
        except:
            with open(os.path.join("users", f'{id_arg}.txt'), 'w') as f:
                f.write(last_name_arg + '\n' + name_arg)
            return "Utilisateur ajouté"

    elif request.method == "PATCH":
        if id_arg is None:
            return "Id Incorrect"
        try:
            with open(os.path.join("users", f'{id_arg}.txt'), 'r') as f:
                user = f.readlines()
                last_name_used, name_used = user[0][0:-1], user[1]
                if name_arg is None:
                    name = name_used
                if last_name_arg is None:
                    last_name = last_name_used

            with open(os.path.join("users", f'{id_arg}.txt'), 'w') as f:
                f.write(f"{last_name}\n{name}")
                return "Utilisateur Modifié"
        except:
            return "Utilisateur Introuvable"

    elif request.method == "DELETE":
        try:
            os.remove(os.path.join("users", f'{id_arg}.txt'))
            return "Utilisateur Supprimé"
        except:
            return "Utilisateur Introuvable"

    return 'None'


if __name__ == '__main__':
    app.run(
        host=host,
        port=8001,
        debug=True
    )
