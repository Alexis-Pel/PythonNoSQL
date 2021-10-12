import os

from flask import Flask
from flask import request
from flask import make_response
app = Flask(__name__)
host = os.environ["HOST"]


@app.route("/")
def main():
    """
    Fonction affichant un titre 'Hi'
    :return: string : Hey You
    """
    return make_response('<h1>Hey You !</h1>', 200)


@app.route("/users", methods=["GET"])
def users():
    if request.method == "GET":
        user_list = []
        for file in os.listdir("users"):
            with open(os.path.join("users", file), 'r') as f:
                user = f.readlines()
                last_name = user[0][0:-1]
                name = user[1]
                title = file.title()
                title = title.split('.')
                title = title[0]
                user_list.append({"id": title, "last_name": last_name, "name": name})
        return make_response(str(list(reversed(user_list))), 200)


@app.route("/users", methods=["POST"])
def post():
    try:
        name_arg = request.args['name']
    except:
        return "Prénom Incorrect"
    try:
        last_name_arg = request.args['last_name']
    except:
        return "Nom Incorrect"
    try:
        id_arg = int(request.args['id'])
    except:
        return "Id Incorrect"

    try:
        open(os.path.join("users", f'{id_arg}.txt'))
        return "Utilisateur déja existant"
    except:
        with open(os.path.join("users", f'{id_arg}.txt'), 'w') as f:
            f.write(last_name_arg + '\n' + name_arg)
        return make_response("Utilisateur ajouté", 200)


@app.route("/users", methods=["PATCH"])
def patch():
    try:
        name_arg = request.args['name']
    except:
        return "Prénom Incorrect"
    try:
        last_name_arg = request.args['last_name']
    except:
        return "Nom Incorrect"
    try:
        id_arg = int(request.args['id'])
    except:
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
            return make_response("Utilisateur Modifié", 200)
    except:
        return "Utilisateur Introuvable"


@app.route("/users", methods=["DELETE"])
def delete():
    try:
        id_arg = int(request.args['id'])
    except:
        return "Id Incorrect"
    try:
        os.remove(os.path.join("users", f'{id_arg}.txt'))
        return make_response("Utilisateur Supprimé", 200)
    except:
        return "Utilisateur Introuvable"


if __name__ == '__main__':
    app.run(
        host=host,
        port=8001,
        debug=True
    )
